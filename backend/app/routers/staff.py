from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_db_admin, get_current_user
from app.core.security import admin_only, require_role
from app.core.exceptions import ResourceNotFoundError, DuplicateResourceError, ValidationError
from app.core.security import get_password_hash
from app.models.staff import Department, Staff, StaffCredential, StaffRoster
from app.schemas.staff import (
    DepartmentCreate, DepartmentRead,
    StaffCreate, StaffRead,
    StaffCredentialCreate, StaffRosterCreate, StaffRosterRead,
)
from app.services.audit_service import log_audit_event

router = APIRouter()


@router.post("/departments", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(
    req: DepartmentCreate,
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(admin_only),
):
    dept = Department(**req.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.get("/departments", response_model=List[DepartmentRead])
def list_departments(
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(get_current_user),
):
    return db.query(Department).filter(Department.is_active == True).all()


@router.post("/", response_model=StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    req: StaffCreate,
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(admin_only),
):
    existing = db.query(Staff).filter(
        (Staff.staff_number == req.staff_number) | (Staff.national_id == req.national_id)
    ).first()
    if existing:
        raise DuplicateResourceError(resource="Staff")

    staff_data = req.model_dump(exclude={"password"})
    staff = Staff(**staff_data)
    db.add(staff)
    db.flush()

    cred = StaffCredential(
        staff_id=staff.staff_id,
        username=req.staff_number.lower(),
        password_hash=get_password_hash(req.password),
    )
    db.add(cred)
    db.commit()
    db.refresh(staff)

    log_audit_event(
        db=db,
        action="STAFF_CREATED",
        entity_type="staff",
        entity_id=staff.staff_id,
        staff_id=current_user.staff_id,
        new_values={"staff_number": staff.staff_number, "role": staff.role},
    )
    return staff


@router.get("/", response_model=List[StaffRead])
def list_staff(
    department_id: Optional[UUID] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(Staff).filter(Staff.is_active == True)
    if department_id:
        query = query.filter(Staff.department_id == department_id)
    if role:
        query = query.filter(Staff.role == role.upper())
    return query.order_by(Staff.last_name).all()


@router.get("/{staff_id}", response_model=StaffRead)
def get_staff(
    staff_id: UUID,
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(get_current_user),
):
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff:
        raise ResourceNotFoundError(resource="Staff")
    return staff


@router.post("/{staff_id}/roster", response_model=StaffRosterRead, status_code=status.HTTP_201_CREATED)
def add_roster(
    staff_id: UUID,
    req: StaffRosterCreate,
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(admin_only),
):
    staff = db.query(Staff).filter(Staff.staff_id == staff_id).first()
    if not staff:
        raise ResourceNotFoundError(resource="Staff")

    roster = StaffRoster(
        **req.model_dump(),
        staff_id=staff_id,
        created_by=current_user.staff_id,
    )
    db.add(roster)
    db.commit()
    db.refresh(roster)
    return roster


@router.get("/{staff_id}/roster", response_model=List[StaffRosterRead])
def get_roster(
    staff_id: UUID,
    db: Session = Depends(get_db_admin),
    current_user: Staff = Depends(get_current_user),
):
    return (
        db.query(StaffRoster)
        .filter(StaffRoster.staff_id == staff_id)
        .order_by(StaffRoster.roster_date.desc())
        .all()
    )