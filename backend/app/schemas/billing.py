from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MedicalAidProviderBase(BaseModel):
    provider_code: str
    provider_name: str
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    claim_submission_url: Optional[str] = None
    is_active: bool = True


class MedicalAidProviderCreate(MedicalAidProviderBase):
    pass


class MedicalAidProviderRead(MedicalAidProviderBase):
    model_config = ConfigDict(from_attributes=True)

    provider_id: UUID
    created_at: datetime


class BillingInvoiceBase(BaseModel):
    invoice_number: str
    patient_id: UUID
    record_id: Optional[UUID] = None
    admission_id: Optional[UUID] = None
    invoice_type: str
    currency_code: str = "USD"
    exchange_rate: str = "1.0"
    subtotal: str = "0"
    discount_amount: str = "0"
    tax_amount: str = "0"
    total_amount: str = "0"
    base_currency_total: str = "0"
    amount_paid: str = "0"
    balance_due: str = "0"
    payment_status: str = "UNPAID"
    medical_aid_claimed: bool = False
    medical_aid_claim_amount: Optional[str] = None
    medical_aid_claim_reference: Optional[str] = None
    due_date: Optional[date] = None


class BillingInvoiceCreate(BillingInvoiceBase):
    pass


class BillingInvoiceRead(BillingInvoiceBase):
    model_config = ConfigDict(from_attributes=True)

    invoice_id: UUID
    invoice_date: datetime
    created_by: Optional[UUID] = None
    created_at: datetime


class InvoiceItemBase(BaseModel):
    invoice_id: UUID
    item_type: str
    reference_id: Optional[UUID] = None
    description: Optional[str] = None
    quantity: Optional[str] = None
    unit_price: Optional[str] = None
    currency_code: str = "USD"
    line_total: Optional[str] = None
    base_currency_line_total: Optional[str] = None


class InvoiceItemCreate(InvoiceItemBase):
    pass


class PaymentBase(BaseModel):
    invoice_id: UUID
    patient_id: UUID
    payment_method: str
    currency_code: str = "USD"
    amount: str
    exchange_rate: str = "1.0"
    base_currency_amount: Optional[str] = None
    reference_number: Optional[str] = None
    received_by: Optional[UUID] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    payment_id: UUID
    payment_date: datetime
    reconciled: bool
    created_at: datetime