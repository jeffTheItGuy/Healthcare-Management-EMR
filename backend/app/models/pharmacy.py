import uuid
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey, UniqueConstraint, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class Medication(Base):
    __tablename__ = "medications"

    medication_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generic_name = Column(String(255), nullable=False)
    brand_name = Column(String(255))
    dosage_form = Column(String(50), nullable=False)
    strength = Column(String(50))
    atc_code = Column(String(10))
    category = Column(String(100))
    reorder_level = Column(Integer)
    reorder_quantity = Column(Integer)
    is_controlled = Column(Boolean, default=False)
    schedule = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PharmacyInventory(Base):
    __tablename__ = "pharmacy_inventory"

    inventory_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.medication_id"))
    total_quantity = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    unit_cost_average = Column(Numeric(18, 4))
    currency_code = Column(String(3), default="USD")
    location_rack = Column(String(50))
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    supplier_code = Column(String(20), unique=True, nullable=False)
    supplier_name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    license_number = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PharmacyBatch(Base):
    __tablename__ = "pharmacy_batches"
    __table_args__ = (UniqueConstraint("medication_id", "batch_number", name="uq_med_batch"),)

    batch_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("pharmacy_inventory.inventory_id"))
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.medication_id"), nullable=False)
    batch_number = Column(String(50), nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.supplier_id"))
    quantity_received = Column(Integer)
    quantity_remaining = Column(Integer)
    unit_cost = Column(Numeric(18, 4))
    currency_code = Column(String(3), default="USD")
    expiry_date = Column(Date)
    manufacturing_date = Column(Date)
    received_date = Column(Date)
    grn_reference = Column(String(50))
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DispensedMedication(Base):
    __tablename__ = "dispensed_medications"

    dispense_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prescription_item_id = Column(UUID(as_uuid=True), ForeignKey("prescription_items.item_id"))
    batch_id = Column(UUID(as_uuid=True), ForeignKey("pharmacy_batches.batch_id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    dispensed_by = Column(UUID(as_uuid=True), ForeignKey("staff.staff_id"))
    quantity_dispensed = Column(Integer)
    unit_price = Column(Numeric(18, 4))
    currency_code = Column(String(3), default="USD")
    total_amount = Column(Numeric(18, 2))
    dispense_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())