from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    patient_number: str
    national_id: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    blood_group: Optional[str] = None
    phone_primary: Optional[str] = None
    phone_secondary: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    suburb: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_aid_provider_id: Optional[UUID] = None
    medical_aid_number: Optional[str] = None
    medical_aid_plan: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    is_active: bool = True


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    patient_id: UUID
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_primary: Optional[str] = None
    phone_secondary: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    suburb: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    medical_aid_provider_id: Optional[UUID] = None
    medical_aid_number: Optional[str] = None
    medical_aid_plan: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    is_active: Optional[bool] = None


class PatientConsentBase(BaseModel):
    patient_id: UUID
    consent_type: str
    consent_given: bool
    consent_document: Optional[str] = None
    valid_from: date
    valid_until: Optional[date] = None


class PatientConsentCreate(PatientConsentBase):
    pass


class PatientConsentRead(PatientConsentBase):
    model_config = ConfigDict(from_attributes=True)

    consent_id: UUID
    revoked_at: Optional[datetime] = None
    created_at: datetime