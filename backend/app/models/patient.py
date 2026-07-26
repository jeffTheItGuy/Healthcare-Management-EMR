import uuid
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_number = Column(String(20), unique=True, nullable=False)
    national_id = Column(String(50))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    blood_group = Column(String(5))
    phone_primary = Column(String(20))
    phone_secondary = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    suburb = Column(String(100))
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    medical_aid_provider_id = Column(UUID(as_uuid=True), ForeignKey("medical_aid_providers.provider_id"))
    medical_aid_number = Column(String(50))
    medical_aid_plan = Column(String(50))
    allergies = Column(Text)
    chronic_conditions = Column(Text)
    is_active = Column(Boolean, default=True)
    deleted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PatientConsent(Base):
    __tablename__ = "patient_consents"

    consent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    consent_type = Column(String(50), nullable=False)
    consent_given = Column(Boolean, nullable=False)
    consent_document = Column(String(500))
    valid_from = Column(Date, nullable=False)
    valid_until = Column(Date)
    revoked_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PatientAccessLog(Base):
    __tablename__ = "patient_access_logs"

    access_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    accessed_by_staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    access_reason = Column(String(255))
    access_type = Column(String(20), nullable=False)
    ip_address = Column(String(45))
    accessed_at = Column(DateTime(timezone=True), server_default=func.now())