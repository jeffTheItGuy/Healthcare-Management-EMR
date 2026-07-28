from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_db_with_rls, get_current_user
from app.core.security import doctor_or_nurse, require_role
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models.admissions import Ward, Bed, Admission
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.admissions import (
    WardCreate, WardRead, BedCreate, BedRead,
    AdmissionCreate, AdmissionRead, AdmissionUpdate,
)
from app.services.audit_service import log_audit_event

router = APIRouter()


@router.post("/wards", response_model=WardRead, status_code=status.HTTP_201_CREATED)
def create_ward(
    req: WardCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(require_role(["ADMIN", "MANAGER"])),
):
    ward = Ward(**req.model_dump())
    db.add(ward)
    db.commit()
    db.refresh(ward)
    return ward


@router.get("/wards", response_model=List[WardRead])
def list_wards(
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    return db.query(Ward).filter(Ward.is_active == True).all()


@router.post("/wards/{ward_id}/beds", response_model=BedRead, status_code=status.HTTP_201_CREATED)
def create_bed(
    ward_id: UUID,
    req: BedCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(require_role(["ADMIN", "MANAGER"])),
):
    ward = db.query(Ward).filter(Ward.ward_id == ward_id).first()
    if not ward:
        raise ResourceNotFoundError(resource="Ward")

    bed = Bed(ward_id=ward_id, **req.model_dump(exclude={"ward_id"}))
    db.add(bed)
    db.commit()
    db.refresh(bed)
    return bed


@router.get("/wards/{ward_id}/beds", response_model=List[BedRead])
def list_beds(
    ward_id: UUID,
    status: Optional[str] = None,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(Bed).filter(Bed.ward_id == ward_id)
    if status:
        query = query.filter(Bed.status == status.upper())
    return query.all()


@router.post("/", response_model=AdmissionRead, status_code=status.HTTP_201_CREATED)
def admit_patient(
    req: AdmissionCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    patient = db.query(Patient).filter(Patient.patient_id == req.patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    bed = db.query(Bed).filter(Bed.bed_id == req.bed_id).first() if req.bed_id else None
    if bed and bed.status != "AVAILABLE":
        raise ValidationError(detail="Selected bed is not available")

    admission = Admission(
        **req.model_dump(),
        admitting_doctor_id=current_user.staff_id,
    )
    db.add(admission)
    db.flush()

    if bed:
        bed.status = "OCCUPIED"
        bed.current_admission_id = admission.admission_id

    db.commit()
    db.refresh(admission)
    return admission


@router.get("/", response_model=List[AdmissionRead])
def list_admissions(
    patient_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(Admission)
    if patient_id:
        query = query.filter(Admission.patient_id == patient_id)
    if status:
        query = query.filter(Admission.status == status.upper())
    return query.order_by(Admission.admission_date.desc()).limit(200).all()


@router.get("/{admission_id}", response_model=AdmissionRead)
def get_admission(
    admission_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    adm = db.query(Admission).filter(Admission.admission_id == admission_id).first()
    if not adm:
        raise ResourceNotFoundError(resource="Admission")
    return adm


@router.post("/{admission_id}/discharge", response_model=AdmissionRead)
def discharge_patient(
    admission_id: UUID,
    req: AdmissionUpdate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    adm = db.query(Admission).filter(Admission.admission_id == admission_id).first()
    if not adm:
        raise ResourceNotFoundError(resource="Admission")
    if adm.status == "DISCHARGED":
        raise ValidationError(detail="Patient already discharged")

    adm.status = "DISCHARGED"
    adm.discharge_date = datetime.now(timezone.utc)
    if req.discharge_type:
        adm.discharge_type = req.discharge_type
    if req.discharge_summary:
        adm.discharge_summary = req.discharge_summary

    # Free the bed
    bed = db.query(Bed).filter(Bed.current_admission_id == admission_id).first()
    if bed:
        bed.status = "AVAILABLE"
        bed.current_admission_id = None

    db.commit()
    db.refresh(adm)
    return adm