from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class WardBase(BaseModel):
    ward_code: str
    ward_name: str
    department_id: Optional[UUID] = None
    ward_type: str
    floor_level: Optional[str] = None
    capacity: Optional[str] = None
    is_active: bool = True


class WardCreate(WardBase):
    pass


class WardRead(WardBase):
    model_config = ConfigDict(from_attributes=True)

    ward_id: UUID
    created_at: datetime


class BedBase(BaseModel):
    ward_id: UUID
    bed_number: str
    bed_type: str
    status: str = "AVAILABLE"
    current_admission_id: Optional[UUID] = None


class BedCreate(BedBase):
    pass


class BedRead(BedBase):
    model_config = ConfigDict(from_attributes=True)

    bed_id: UUID
    created_at: datetime


class AdmissionBase(BaseModel):
    patient_id: UUID
    bed_id: Optional[UUID] = None
    admitting_doctor_id: Optional[UUID] = None
    admission_number: str
    admission_type: str
    discharge_date: Optional[datetime] = None
    discharge_type: Optional[str] = None
    discharge_summary: Optional[str] = None
    status: str = "ADMITTED"


class AdmissionCreate(AdmissionBase):
    pass


class AdmissionRead(AdmissionBase):
    model_config = ConfigDict(from_attributes=True)

    admission_id: UUID
    admission_date: datetime
    created_at: datetime


class AdmissionUpdate(BaseModel):
    bed_id: Optional[UUID] = None
    discharge_date: Optional[datetime] = None
    discharge_type: Optional[str] = None
    discharge_summary: Optional[str] = None
    status: Optional[str] = None