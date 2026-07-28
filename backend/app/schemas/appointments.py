from datetime import datetime, date, time
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    patient_id: UUID
    doctor_id: Optional[UUID] = None
    department_id: Optional[UUID] = None
    appointment_number: str
    scheduled_date: date
    scheduled_time: Optional[time] = None
    estimated_duration_minutes: Optional[int] = None
    appointment_type: str
    status: str = "SCHEDULED"
    chief_complaint: Optional[str] = None
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    appointment_id: UUID
    checked_in_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    created_at: datetime


class AppointmentUpdate(BaseModel):
    doctor_id: Optional[UUID] = None
    department_id: Optional[UUID] = None
    appointment_number: Optional[str] = None
    scheduled_date: Optional[date] = None
    scheduled_time: Optional[time] = None
    estimated_duration_minutes: Optional[int] = None
    appointment_type: Optional[str] = None
    status: Optional[str] = None
    chief_complaint: Optional[str] = None
    notes: Optional[str] = None