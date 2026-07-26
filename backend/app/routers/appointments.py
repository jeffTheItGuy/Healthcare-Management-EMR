from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.dependencies import get_db_with_rls, get_current_user
from app.core.security import doctor_or_nurse
from app.core.exceptions import ResourceNotFoundError
from app.models.appointments import Appointment
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.appointments import AppointmentCreate, AppointmentRead, AppointmentUpdate
from app.services.audit_service import log_audit_event

router = APIRouter()


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
def create_appointment(
    req: AppointmentCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    patient = db.query(Patient).filter(Patient.patient_id == req.patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    appt = Appointment(**req.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


@router.get("/", response_model=List[AppointmentRead])
def list_appointments(
    patient_id: Optional[UUID] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(Appointment)
    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)
    if date_from:
        query = query.filter(Appointment.appointment_date >= date_from)
    if date_to:
        query = query.filter(Appointment.appointment_date <= date_to)
    if status:
        query = query.filter(Appointment.status == status.upper())
    return query.order_by(Appointment.appointment_date.desc()).limit(200).all()


@router.get("/{appointment_id}", response_model=AppointmentRead)
def get_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise ResourceNotFoundError(resource="Appointment")
    return appt


@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(
    appointment_id: UUID,
    req: AppointmentUpdate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise ResourceNotFoundError(resource="Appointment")

    for field, value in req.model_dump(exclude_unset=True).items():
        setattr(appt, field, value)

    db.commit()
    db.refresh(appt)
    return appt


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    appt = db.query(Appointment).filter(Appointment.appointment_id == appointment_id).first()
    if not appt:
        raise ResourceNotFoundError(resource="Appointment")

    appt.status = "CANCELLED"
    db.commit()
    return None