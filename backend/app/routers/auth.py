from datetime import timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.staff import Staff, StaffCredential
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
    get_current_user,
)
from app.core.exceptions import AuthenticationError, DuplicateResourceError, ValidationError
from app.services.audit_service import log_audit_event
from app.schemas.staff import StaffRead

router = APIRouter()

security_scheme = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    """Authenticate staff and return JWT."""
    cred = (
        db.query(StaffCredential)
        .filter(StaffCredential.username == req.username)
        .first()
    )
    if not cred:
        raise AuthenticationError(detail="Invalid username or password")

    staff = db.query(Staff).filter(Staff.staff_id == cred.staff_id).first()
    if not staff or not staff.is_active:
        raise AuthenticationError(detail="Account inactive")

    if cred.locked_until and cred.locked_until > datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked",
        )

    if not verify_password(req.password, cred.password_hash):
        # Increment failed attempts
        attempts = int(cred.failed_login_attempts or "0") + 1
        cred.failed_login_attempts = str(attempts)
        if attempts >= 5:
            cred.locked_until = datetime.now(timezone.utc) + timedelta(minutes=30)
        db.commit()
        raise AuthenticationError(detail="Invalid username or password")

    # Success: reset attempts
    cred.failed_login_attempts = "0"
    cred.locked_until = None
    cred.last_login_at = datetime.now(timezone.utc)
    db.commit()

    token = create_access_token(
        data={"sub": str(staff.staff_id), "role": staff.role},
        expires_delta=timedelta(minutes=480),
    )

    log_audit_event(
        db=db,
        action="LOGIN",
        entity_type="staff_credentials",
        entity_id=cred.credential_id,
        staff_id=staff.staff_id,
        ip_address=request.client.host if request.client else None,
    )

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        expires_in=480 * 60,
    )


@router.get("/me", response_model=StaffRead)
def me(current_user: Staff = Depends(get_current_user)):
    """Return current authenticated staff profile."""
    return current_user


@router.post("/change-password")
def change_password(
    req: PasswordChangeRequest,
    request: Request,
    current_user: Staff = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change password for authenticated user."""
    cred = (
        db.query(StaffCredential)
        .filter(StaffCredential.staff_id == current_user.staff_id)
        .first()
    )
    if not cred or not verify_password(req.old_password, cred.password_hash):
        raise AuthenticationError(detail="Old password is incorrect")

    if len(req.new_password) < 8:
        raise ValidationError(detail="Password must be at least 8 characters")

    cred.password_hash = get_password_hash(req.new_password)
    cred.password_changed_at = datetime.now(timezone.utc)
    db.commit()

    log_audit_event(
        db=db,
        action="PASSWORD_CHANGED",
        entity_type="staff_credentials",
        entity_id=cred.credential_id,
        staff_id=current_user.staff_id,
        ip_address=request.client.host if request.client else None,
    )

    return {"detail": "Password updated successfully"}