from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_db_with_rls, get_current_user
from app.core.security import doctor_or_nurse
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models.medical import MedicalRecord, Diagnosis, Prescription, PrescriptionItem
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.medical import (
    MedicalRecordCreate, MedicalRecordRead,
    DiagnosisCreate, PrescriptionCreate, PrescriptionItemCreate,
)
from app.services.audit_service import log_audit_event

router = APIRouter()


@router.post("/", response_model=MedicalRecordRead, status_code=status.HTTP_201_CREATED)
def create_record(
    req: MedicalRecordCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    patient = db.query(Patient).filter(Patient.patient_id == req.patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    record = MedicalRecord(
        **req.model_dump(),
        attending_doctor_id=current_user.staff_id if current_user.role == "DOCTOR" else req.attending_doctor_id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{record_id}", response_model=MedicalRecordRead)
def get_record(
    record_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not record:
        raise ResourceNotFoundError(resource="Medical record")
    return record


@router.post("/{record_id}/diagnoses", status_code=status.HTTP_201_CREATED)
def add_diagnosis(
    record_id: UUID,
    req: DiagnosisCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not record:
        raise ResourceNotFoundError(resource="Medical record")
    if record.is_locked:
        raise ValidationError(detail="Record is locked")

    diag = Diagnosis(
        **req.model_dump(),
        record_id=record_id,
        diagnosed_by=current_user.staff_id,
    )
    db.add(diag)
    db.commit()
    db.refresh(diag)
    return diag


@router.post("/{record_id}/prescriptions", status_code=status.HTTP_201_CREATED)
def add_prescription(
    record_id: UUID,
    req: PrescriptionCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not record:
        raise ResourceNotFoundError(resource="Medical record")
    if record.is_locked:
        raise ValidationError(detail="Record is locked")

    rx = Prescription(
        **req.model_dump(),
        record_id=record_id,
        prescribed_by=current_user.staff_id,
    )
    db.add(rx)
    db.commit()
    db.refresh(rx)
    return rx


@router.post("/{record_id}/lock", status_code=status.HTTP_200_OK)
def lock_record(
    record_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    record = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
    if not record:
        raise ResourceNotFoundError(resource="Medical record")

    record.is_locked = True
    record.locked_by = current_user.staff_id
    record.locked_at = datetime.now(timezone.utc)
    db.commit()
    return {"detail": "Record locked"}