from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    patient_id: UUID
    staff_id: Optional[UUID] = None
    appointment_date: datetime
    appointment_type: str
    status: str = "SCHEDULED"
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)

    appointment_id: UUID
    created_at: datetime


class AppointmentUpdate(BaseModel):
    staff_id: Optional[UUID] = None
    appointment_date: Optional[datetime] = None
    appointment_type: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None