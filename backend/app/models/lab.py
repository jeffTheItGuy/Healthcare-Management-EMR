import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class LabTestCatalog(Base):
    __tablename__ = "lab_test_catalog"

    test_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_code = Column(String(20), unique=True, nullable=False)
    test_name = Column(String(255), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    sample_type = Column(String(50))
    turnaround_hours = Column(Integer)
    normal_range = Column(Text)
    unit_of_measure = Column(String(20))
    base_price = Column(Numeric(18, 2))
    currency_code = Column(String(3), default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LabOrder(Base):
    __tablename__ = "lab_orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(20), unique=True, nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.record_id"))
    ordered_by = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    priority = Column(String(20), default="ROUTINE")
    status = Column(String(20), default="ORDERED")
    clinical_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LabOrderItem(Base):
    __tablename__ = "lab_order_items"

    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("lab_orders.order_id"))
    test_id = Column(UUID(as_uuid=True), ForeignKey("lab_test_catalog.test_id"))
    status = Column(String(20), default="PENDING")
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LabResult(Base):
    __tablename__ = "lab_results"

    result_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey("lab_order_items.order_item_id"))
    test_id = Column(UUID(as_uuid=True), ForeignKey("lab_test_catalog.test_id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    result_value = Column(String(255))
    result_numeric = Column(String(20))
    unit_of_measure = Column(String(20))
    reference_range = Column(Text)
    interpretation = Column(String(20))
    verified_by = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    verified_at = Column(DateTime(timezone=True))
    result_notes = Column(Text)
    is_critical = Column(Boolean, default=False)
    critical_notified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())