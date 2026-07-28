from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MedicalRecordBase(BaseModel):
    patient_id: UUID
    appointment_id: Optional[UUID] = None
    admission_id: Optional[UUID] = None
    encounter_type: str
    attending_doctor_id: Optional[UUID] = None
    nurse_id: Optional[UUID] = None
    chief_complaint: Optional[str] = None
    history_of_present_illness: Optional[str] = None
    physical_examination: Optional[str] = None
    vital_signs: Optional[Dict[str, Any]] = None
    assessment_and_plan: Optional[str] = None
    discharge_notes: Optional[str] = None
    follow_up_instructions: Optional[str] = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordRead(MedicalRecordBase):
    model_config = ConfigDict(from_attributes=True)

    record_id: UUID
    encounter_date: datetime
    is_locked: bool
    locked_by: Optional[UUID] = None
    locked_at: Optional[datetime] = None
    created_at: datetime


class DiagnosisBase(BaseModel):
    record_id: UUID
    icd10_code: Optional[str] = None
    diagnosis_name: str
    diagnosis_type: str
    notes: Optional[str] = None
    diagnosed_by: Optional[UUID] = None


class DiagnosisCreate(DiagnosisBase):
    pass


class PrescriptionBase(BaseModel):
    record_id: UUID
    patient_id: UUID
    prescribed_by: Optional[UUID] = None
    status: str = "PENDING"
    pharmacy_notes: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionItemBase(BaseModel):
    prescription_id: UUID
    medication_id: UUID
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration_days: Optional[int] = None
    quantity_prescribed: Optional[str] = None
    quantity_dispensed: Optional[str] = None
    instructions: Optional[str] = None
    is_substitutable: bool = False


class PrescriptionItemCreate(PrescriptionItemBase):
    pass