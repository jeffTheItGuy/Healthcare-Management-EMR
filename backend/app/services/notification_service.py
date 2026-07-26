"""Notification service for critical alerts."""
import logging
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.lab import LabResult
from app.models.staff import Staff

logger = logging.getLogger(__name__)


def notify_critical_lab_result(db: Session, result: LabResult) -> None:
    """
    Trigger notification for critical lab results.
    In production: integrate with SMS gateway (Twilio, Africa's Talking, local SMS API)
    or hospital paging system.
    """
    if not result.is_critical:
        return

    # Get attending doctor
    doctor = db.query(Staff).filter(Staff.staff_id == result.verified_by).first()
    doctor_name = f"{doctor.first_name} {doctor.last_name}" if doctor else "Unknown"

    message = (
        f"CRITICAL LAB ALERT\n"
        f"Patient: {result.patient_id}\n"
        f"Test: {result.test_id}\n"
        f"Result: {result.result_value} {result.unit_of_measure or ''}\n"
        f"Interpretation: {result.interpretation}\n"
        f"Verified by: {doctor_name}\n"
        f"Time: {datetime.now().isoformat()}"
    )

    # Placeholder for actual SMS/email integration
    # In Zimbabwe, you might use:
    # - Africa's Talking SMS API
    # - Econet/NetOne bulk SMS gateway
    # - Hospital internal paging system
    
    logger.warning(f"CRITICAL ALERT: {message}")
    
    # Mark as notified
    result.critical_notified_at = datetime.utcnow()
    db.commit()


def notify_low_stock(medication_name: str, current_qty: int, reorder_level: int) -> None:
    """Alert pharmacy manager when stock falls below reorder level."""
    logger.warning(
        f"LOW STOCK ALERT: {medication_name} "
        f"(current: {current_qty}, reorder at: {reorder_level})"
    )
    # TODO: Send email/SMS to pharmacy manager