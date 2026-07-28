from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_db_with_rls, get_current_user, get_db_admin
from app.core.security import cashier_or_admin, require_role
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models.billing import BillingInvoice, InvoiceItem, Payment, MedicalAidProvider
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.billing import (
    BillingInvoiceCreate, BillingInvoiceRead,
    InvoiceItemCreate, PaymentCreate, PaymentRead,
    MedicalAidProviderCreate, MedicalAidProviderRead,
)
from app.services.billing_service import calculate_invoice_totals, apply_payment
from app.services.audit_service import log_audit_event

router = APIRouter()


@router.post("/providers", response_model=MedicalAidProviderRead, status_code=status.HTTP_201_CREATED)
def create_provider(
    req: MedicalAidProviderCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(require_role(["ADMIN", "MANAGER"])),
):
    provider = MedicalAidProvider(**req.model_dump())
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@router.get("/providers", response_model=List[MedicalAidProviderRead])
def list_providers(
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    return db.query(MedicalAidProvider).filter(MedicalAidProvider.is_active == True).all()


@router.post("/invoices", response_model=BillingInvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(
    req: BillingInvoiceCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(cashier_or_admin),
):
    patient = db.query(Patient).filter(Patient.patient_id == req.patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    invoice = BillingInvoice(
        **req.model_dump(),
        created_by=current_user.staff_id,
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.get("/invoices", response_model=List[BillingInvoiceRead])
def list_invoices(
    patient_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(BillingInvoice)
    if patient_id:
        query = query.filter(BillingInvoice.patient_id == patient_id)
    if status:
        query = query.filter(BillingInvoice.payment_status == status.upper())
    return query.order_by(BillingInvoice.invoice_date.desc()).limit(200).all()


@router.get("/invoices/{invoice_id}", response_model=BillingInvoiceRead)
def get_invoice(
    invoice_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    invoice = db.query(BillingInvoice).filter(BillingInvoice.invoice_id == invoice_id).first()
    if not invoice:
        raise ResourceNotFoundError(resource="Invoice")
    return invoice


@router.post("/invoices/{invoice_id}/items", status_code=status.HTTP_201_CREATED)
def add_invoice_item(
    invoice_id: UUID,
    req: InvoiceItemCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(cashier_or_admin),
):
    invoice = db.query(BillingInvoice).filter(BillingInvoice.invoice_id == invoice_id).first()
    if not invoice:
        raise ResourceNotFoundError(resource="Invoice")

    item = InvoiceItem(invoice_id=invoice_id, **req.model_dump())
    db.add(item)
    db.commit()

    # Recalculate totals
    db.refresh(invoice)
    calculate_invoice_totals(invoice)
    db.commit()
    db.refresh(invoice)

    return item


@router.post("/invoices/{invoice_id}/payments", response_model=BillingInvoiceRead)
def add_payment(
    invoice_id: UUID,
    req: PaymentCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(cashier_or_admin),
):
    payment = Payment(
        **req.model_dump(),
        received_by=current_user.staff_id,
    )
    invoice = apply_payment(db, invoice_id, payment)
    return invoice