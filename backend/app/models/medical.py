import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.appointment_id"))
    admission_id = Column(UUID(as_uuid=True), ForeignKey("admissions.admission_id"))
    encounter_type = Column(String(20), nullable=False)
    attending_doctor_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    nurse_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    encounter_date = Column(DateTime(timezone=True), server_default=func.now())
    chief_complaint = Column(Text)
    history_of_present_illness = Column(Text)
    physical_examination = Column(Text)
    vital_signs = Column(JSON)
    assessment_and_plan = Column(Text)
    discharge_notes = Column(Text)
    follow_up_instructions = Column(Text)
    is_locked = Column(Boolean, default=False)
    locked_by = Column(UUID(as_uuid=True))
    locked_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    diagnosis_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.record_id"))
    icd10_code = Column(String(10))
    diagnosis_name = Column(String(255), nullable=False)
    diagnosis_type = Column(String(20), nullable=False)
    notes = Column(Text)
    diagnosed_by = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prescription(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.record_id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    prescribed_by = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    prescription_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="PENDING")
    pharmacy_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PrescriptionItem(Base):
    __tablename__ = "prescription_items"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prescription_id = Column(UUID(as_uuid=True), ForeignKey("prescriptions.prescription_id"))
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.medication_id"))
    dosage = Column(String(100))
    frequency = Column(String(100))
    duration_days = Column(String(20))
    quantity_prescribed = Column(String(20))
    quantity_dispensed = Column(String(20))
    instructions = Column(Text)
    is_substitutable = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())