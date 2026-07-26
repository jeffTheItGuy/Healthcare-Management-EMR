"""Billing calculations with multi-currency support."""
from decimal import Decimal, ROUND_HALF_UP
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.billing import BillingInvoice, InvoiceItem, Payment
from app.services.audit_service import log_audit_event


def to_decimal(value) -> Decimal:
    """Safely convert string/numeric to Decimal."""
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


def calculate_invoice_totals(invoice: BillingInvoice) -> BillingInvoice:
    """Recalculate subtotal, tax, discount, balance from line items."""
    items: List[InvoiceItem] = invoice.items if hasattr(invoice, "items") else []
    
    subtotal = Decimal("0")
    for item in items:
        qty = to_decimal(item.quantity)
        price = to_decimal(item.unit_price)
        line_total = (qty * price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        item.line_total = str(line_total)
        
        # Convert to base currency (assume exchange_rate on invoice)
        rate = to_decimal(invoice.exchange_rate)
        base_line = (line_total * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        item.base_currency_line_total = str(base_line)
        
        subtotal += line_total

    discount = to_decimal(invoice.discount_amount)
    tax = to_decimal(invoice.tax_amount)
    total = (subtotal - discount + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    base_rate = to_decimal(invoice.exchange_rate)
    base_total = (total * base_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    paid = to_decimal(invoice.amount_paid)
    balance = (total - paid).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Auto-set payment status
    if balance <= 0:
        payment_status = "PAID"
    elif paid > 0:
        payment_status = "PARTIAL"
    else:
        payment_status = "UNPAID"

    invoice.subtotal = str(subtotal)
    invoice.total_amount = str(total)
    invoice.base_currency_total = str(base_total)
    invoice.balance_due = str(balance)
    invoice.payment_status = payment_status

    return invoice


def apply_payment(db: Session, invoice_id: UUID, payment: Payment) -> BillingInvoice:
    """Apply a payment to an invoice and recalculate balance."""
    invoice = db.query(BillingInvoice).filter(BillingInvoice.invoice_id == invoice_id).first()
    if not invoice:
        raise ValueError("Invoice not found")

    current_paid = to_decimal(invoice.amount_paid)
    payment_amount = to_decimal(payment.amount)
    new_paid = (current_paid + payment_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    invoice.amount_paid = str(new_paid)
    
    # Recalculate
    invoice = calculate_invoice_totals(invoice)
    
    db.add(payment)
    db.commit()
    db.refresh(invoice)
    
    # Audit log
    log_audit_event(
        db=db,
        action="PAYMENT_APPLIED",
        entity_type="billing_invoices",
        entity_id=invoice_id,
        staff_id=payment.received_by,
        new_values={
            "payment_id": str(payment.payment_id),
            "amount": str(payment_amount),
            "method": payment.payment_method,
            "new_balance": invoice.balance_due,
        },
    )
    
    return invoice