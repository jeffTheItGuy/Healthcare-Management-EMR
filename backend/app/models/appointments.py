import uuid
from sqlalchemy import Column, String, Text, DateTime, Date, Time, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_number = Column(String(20), unique=True, nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.department_id"))
    appointment_type = Column(String(50), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    scheduled_time = Column(Time)
    estimated_duration_minutes = Column(Integer)
    status = Column(String(20), default="SCHEDULED")
    chief_complaint = Column(Text)
    notes = Column(Text)
    checked_in_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())