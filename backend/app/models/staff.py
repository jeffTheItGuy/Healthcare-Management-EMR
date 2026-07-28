import uuid
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_code = Column(String(20), unique=True, nullable=False)
    department_name = Column(String(100), nullable=False)
    department_type = Column(String(50), nullable=False)
    location = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_number = Column(String(20), unique=True, nullable=False)
    national_id = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.department_id"))
    specialization = Column(String(100))
    license_number = Column(String(50))
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StaffCredential(Base):
    __tablename__ = "staff_credentials"

    credential_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id", ondelete="CASCADE"))
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    mfa_enabled = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True))
    password_changed_at = Column(DateTime(timezone=True))
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StaffRoster(Base):
    __tablename__ = "staff_rosters"
    __table_args__ = (UniqueConstraint("staff_id", "roster_date", "shift_type", name="uq_staff_roster"),)

    roster_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.department_id"))
    roster_date = Column(Date, nullable=False)
    shift_type = Column(String(20), nullable=False)
    start_time = Column(String(8))
    end_time = Column(String(8))
    ward_id = Column(UUID(as_uuid=True), ForeignKey("wards.ward_id"))
    notes = Column(Text)
    created_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())