import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    appointment_date = Column(DateTime(timezone=True), nullable=False)
    appointment_type = Column(String(50), nullable=False)
    status = Column(String(20), default="SCHEDULED")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())