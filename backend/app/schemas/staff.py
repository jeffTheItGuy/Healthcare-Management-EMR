from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class DepartmentBase(BaseModel):
    department_code: str
    department_name: str
    department_type: str
    location: Optional[str] = None
    is_active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    model_config = ConfigDict(from_attributes=True)

    department_id: UUID
    created_at: datetime


class StaffBase(BaseModel):
    staff_number: str
    national_id: str
    first_name: str
    last_name: str
    role: str
    department_id: Optional[UUID] = None
    specialization: Optional[str] = None
    license_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True


class StaffCreate(StaffBase):
    password: str  # Plain password for initial creation only


class StaffRead(StaffBase):
    model_config = ConfigDict(from_attributes=True)

    staff_id: UUID
    created_at: datetime


class StaffCredentialBase(BaseModel):
    staff_id: UUID
    username: str
    mfa_enabled: bool = False


class StaffCredentialCreate(BaseModel):
    staff_id: UUID
    username: str
    password: str


class StaffRosterBase(BaseModel):
    staff_id: UUID
    department_id: Optional[UUID] = None
    roster_date: date
    shift_type: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    ward_id: Optional[UUID] = None
    notes: Optional[str] = None


class StaffRosterCreate(StaffRosterBase):
    pass


class StaffRosterRead(StaffRosterBase):
    model_config = ConfigDict(from_attributes=True)

    roster_id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime