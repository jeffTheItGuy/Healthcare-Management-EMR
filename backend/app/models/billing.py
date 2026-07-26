import uuid
from sqlalchemy import Column, String, Text, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base


class MedicalAidProvider(Base):
    __tablename__ = "medical_aid_providers"

    provider_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_code = Column(String(20), unique=True, nullable=False)
    provider_name = Column(String(200), nullable=False)
    contact_phone = Column(String(20))
    contact_email = Column(String(255))
    claim_submission_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BillingInvoice(Base):
    __tablename__ = "billing_invoices"

    invoice_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_number = Column(String(50), unique=True, nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    record_id = Column(UUID(as_uuid=True), ForeignKey("medical_records.record_id"))
    admission_id = Column(UUID(as_uuid=True), ForeignKey("admissions.admission_id"))
    invoice_type = Column(String(20), nullable=False)
    currency_code = Column(String(3), default="USD")
    exchange_rate = Column(String(30), default="1.0")
    subtotal = Column(String(20), default="0")
    discount_amount = Column(String(20), default="0")
    tax_amount = Column(String(20), default="0")
    total_amount = Column(String(20), default="0")
    base_currency_total = Column(String(20), default="0")
    amount_paid = Column(String(20), default="0")
    balance_due = Column(String(20), default="0")
    payment_status = Column(String(20), default="UNPAID")
    medical_aid_claimed = Column(Boolean, default=False)
    medical_aid_claim_amount = Column(String(20))
    medical_aid_claim_reference = Column(String(50))
    invoice_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(Date)
    created_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("billing_invoices.invoice_id"))
    item_type = Column(String(50), nullable=False)
    reference_id = Column(UUID(as_uuid=True))
    description = Column(Text)
    quantity = Column(String(20))
    unit_price = Column(String(20))
    currency_code = Column(String(3), default="USD")
    line_total = Column(String(20))
    base_currency_line_total = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("billing_invoices.invoice_id"))
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"))
    payment_method = Column(String(50), nullable=False)
    currency_code = Column(String(3), default="USD")
    amount = Column(String(20), nullable=False)
    exchange_rate = Column(String(30), default="1.0")
    base_currency_amount = Column(String(20))
    reference_number = Column(String(100))
    received_by = Column(UUID(as_uuid=True))
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    reconciled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())