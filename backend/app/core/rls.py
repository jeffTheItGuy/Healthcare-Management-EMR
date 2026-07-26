"""PostgreSQL Row Level Security context helpers.

RLS policies in ZimEMR rely on session-level variables set per request.
Before executing queries on RLS-protected tables, call these setters.
"""
from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session


def set_staff_rls_context(db: Session, staff_id: UUID) -> None:
    """Set the current staff ID for RLS policy evaluation."""
    db.execute(
        text("SET LOCAL app.current_staff_id = :staff_id"),
        {"staff_id": str(staff_id)},
    )


def set_patient_rls_context(db: Session, patient_id: UUID) -> None:
    """Set the current patient ID for self-access RLS policy evaluation."""
    db.execute(
        text("SET LOCAL app.current_patient_id = :patient_id"),
        {"patient_id": str(patient_id)},
    )


def clear_rls_context(db: Session) -> None:
    """Clear RLS session variables (useful for admin operations)."""
    db.execute(text("RESET app.current_staff_id"))
    db.execute(text("RESET app.current_patient_id"))