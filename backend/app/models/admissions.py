import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Ward(Base):
    __tablename__ = "wards"

    ward_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ward_code = Column(String(20), unique=True, nullable=False)
    ward_name = Column(String(100), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.department_id"))
    ward_type = Column(String(50), nullable=False)
    floor_level = Column(String(20))
    capacity = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Bed(Base):
    __tablename__ = "beds"
    __table_args__ = (UniqueConstraint("ward_id", "bed_number", name="uq_ward_bed"),)

    bed_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ward_id = Column(UUID(as_uuid=True), ForeignKey("wards.ward_id"), nullable=False)
    bed_number = Column(String(20), nullable=False)
    bed_type = Column(String(50), nullable=False)
    status = Column(String(20), default="AVAILABLE")
    current_admission_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Admission(Base):
    __tablename__ = "admissions"

    admission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    bed_id = Column(UUID(as_uuid=True), ForeignKey("beds.bed_id"))
    admitting_doctor_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    admission_number = Column(String(20), unique=True, nullable=False)
    admission_type = Column(String(20), nullable=False)
    admission_date = Column(DateTime(timezone=True), server_default=func.now())
    discharge_date = Column(DateTime(timezone=True))
    discharge_type = Column(String(20))
    discharge_summary = Column(Text)
    status = Column(String(20), default="ADMITTED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())