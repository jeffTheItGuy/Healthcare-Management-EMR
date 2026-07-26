from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.database import get_db
from app.dependencies import get_db_with_rls, get_current_user, get_db_admin
from app.core.security import require_role, doctor_or_nurse
from app.core.exceptions import ResourceNotFoundError, DuplicateResourceError, ValidationError
from app.models.patient import Patient, PatientConsent
from app.models.staff import Staff
from app.schemas.patient import (
    PatientCreate, PatientRead, PatientUpdate,
    PatientConsentCreate, PatientConsentRead,
)
from app.services.audit_service import log_audit_event
from app.utils.validators import validate_phone_zw, validate_zimbabwe_national_id

router = APIRouter()


def _log_access(db: Session, patient_id: UUID, staff: Staff, reason: str, ip: Optional[str]):
    log_audit_event(
        db=db,
        action="PATIENT_ACCESS",
        entity_type="patients",
        entity_id=patient_id,
        staff_id=staff.staff_id,
        ip_address=ip,
    )


@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(
    req: PatientCreate,
    request: Request,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    if req.national_id and not validate_zimbabwe_national_id(req.national_id):
        raise ValidationError(detail="Invalid national ID format")
    if not validate_phone_zw(req.phone_primary):
        raise ValidationError(detail="Invalid primary phone number")

    existing = db.query(Patient).filter(
        or_(
            Patient.patient_number == req.patient_number,
            Patient.national_id == req.national_id,
        )
    ).first()
    if existing:
        raise DuplicateResourceError(resource="Patient")

    patient = Patient(**req.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)

    log_audit_event(
        db=db,
        action="PATIENT_CREATED",
        entity_type="patients",
        entity_id=patient.patient_id,
        staff_id=current_user.staff_id,
        new_values=req.model_dump(),
        ip_address=request.client.host if request.client else None,
    )
    return patient


@router.get("/", response_model=List[PatientRead])
def list_patients(
    q: Optional[str] = Query(None, description="Search by name, phone, or patient number"),
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(Patient).filter(Patient.deleted_at.is_(None))
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                Patient.first_name.ilike(search),
                Patient.last_name.ilike(search),
                Patient.phone_primary.ilike(search),
                Patient.patient_number.ilike(search),
                Patient.national_id.ilike(search),
            )
        )
    return query.order_by(Patient.created_at.desc()).limit(100).all()


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: UUID,
    request: Request,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    patient = db.query(Patient).filter(
        Patient.patient_id == patient_id,
        Patient.deleted_at.is_(None),
    ).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    _log_access(db, patient_id, current_user, "VIEW", request.client.host if request.client else None)
    return patient


@router.put("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: UUID,
    req: PatientUpdate,
    request: Request,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    patient = db.query(Patient).filter(
        Patient.patient_id == patient_id,
        Patient.deleted_at.is_(None),
    ).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    update_data = req.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    log_audit_event(
        db=db,
        action="PATIENT_UPDATED",
        entity_type="patients",
        entity_id=patient_id,
        staff_id=current_user.staff_id,
        new_values=update_data,
        ip_address=request.client.host if request.client else None,
    )
    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: UUID,
    request: Request,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(require_role(["ADMIN", "MANAGER"])),
):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    patient.is_active = False
    patient.deleted_at = func.now()
    db.commit()

    log_audit_event(
        db=db,
        action="PATIENT_DELETED",
        entity_type="patients",
        entity_id=patient_id,
        staff_id=current_user.staff_id,
        ip_address=request.client.host if request.client else None,
    )
    return None


@router.post("/{patient_id}/consents", response_model=PatientConsentRead, status_code=status.HTTP_201_CREATED)
def add_consent(
    patient_id: UUID,
    req: PatientConsentCreate,
    request: Request,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    consent = PatientConsent(patient_id=patient_id, **req.model_dump())
    db.add(consent)
    db.commit()
    db.refresh(consent)

    log_audit_event(
        db=db,
        action="CONSENT_ADDED",
        entity_type="patient_consents",
        entity_id=consent.consent_id,
        staff_id=current_user.staff_id,
        ip_address=request.client.host if request.client else None,
    )
    return consent


@router.get("/{patient_id}/consents", response_model=List[PatientConsentRead])
def list_consents(
    patient_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    return db.query(PatientConsent).filter(PatientConsent.patient_id == patient_id).all()