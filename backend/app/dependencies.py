"""FastAPI dependency injection utilities."""
from typing import Generator, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.core.security import get_current_user, decode_access_token
from app.core.rls import set_staff_rls_context, set_patient_rls_context
from app.models.staff import Staff


def get_db_with_rls(
    request: Request,
    current_user: Staff = Depends(get_current_user),
) -> Generator[Session, None, None]:
    """
    Database dependency that automatically sets RLS context
    for the current authenticated user before yielding the session.
    Use this instead of plain get_db() for all patient/record endpoints.
    """
    db = SessionLocal()
    try:
        set_staff_rls_context(db, current_user.staff_id)
        yield db
    finally:
        db.close()


def get_db_admin(
    current_user: Staff = Depends(get_current_user),
) -> Generator[Session, None, None]:
    """
    Database dependency for admin operations that bypasses RLS.
    Only use for admin/manager endpoints that need cross-department visibility.
    """
    if current_user.role not in ("ADMIN", "MANAGER"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin database access required",
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_staff_id(
    current_user: Staff = Depends(get_current_user),
) -> UUID:
    """Dependency that returns just the current staff UUID."""
    return current_user.staff_id


def get_current_staff_role(
    current_user: Staff = Depends(get_current_user),
) -> str:
    """Dependency that returns just the current staff role."""
    return current_user.role


def get_optional_user(
    request: Request,
    db: Session = Depends(get_db),
) -> Optional[Staff]:
    """
    Attempt to get the current user from token, but don't fail if missing.
    Useful for endpoints that have both public and authenticated behavior.
    """
    auth_header = request.headers.get("authorization")
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]
    payload = decode_access_token(token)
    if not payload:
        return None

    staff_id_str = payload.get("sub")
    if not staff_id_str:
        return None

    try:
        staff_id = UUID(staff_id_str)
    except ValueError:
        return None

    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if staff and staff.is_active:
        return staff
    return None