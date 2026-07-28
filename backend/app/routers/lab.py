from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_db_with_rls, get_current_user
from app.core.security import doctor_or_nurse, lab_tech_only, require_role
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.models.lab import LabTestCatalog, LabOrder, LabOrderItem, LabResult
from app.models.patient import Patient
from app.models.staff import Staff
from app.schemas.lab import (
    LabTestCatalogCreate, LabTestCatalogRead,
    LabOrderCreate, LabOrderRead,
    LabResultCreate, LabResultRead,
)
from app.services.audit_service import log_audit_event
from app.services.notification_service import notify_critical_lab_result

router = APIRouter()


@router.post("/catalog", response_model=LabTestCatalogRead, status_code=status.HTTP_201_CREATED)
def create_test_catalog(
    req: LabTestCatalogCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(require_role(["ADMIN", "MANAGER", "LAB_TECH"])),
):
    test = LabTestCatalog(**req.model_dump())
    db.add(test)
    db.commit()
    db.refresh(test)
    return test


@router.get("/catalog", response_model=List[LabTestCatalogRead])
def list_catalog(
    category: Optional[str] = None,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(LabTestCatalog).filter(LabTestCatalog.is_active == True)
    if category:
        query = query.filter(LabTestCatalog.category.ilike(f"%{category}%"))
    return query.all()


@router.post("/orders", response_model=LabOrderRead, status_code=status.HTTP_201_CREATED)
def create_lab_order(
    req: LabOrderCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(doctor_or_nurse),
):
    patient = db.query(Patient).filter(Patient.patient_id == req.patient_id).first()
    if not patient:
        raise ResourceNotFoundError(resource="Patient")

    order = LabOrder(
        **req.model_dump(exclude={"ordered_by"}),
        ordered_by=current_user.staff_id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/orders", response_model=List[LabOrderRead])
def list_orders(
    patient_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    query = db.query(LabOrder)
    if patient_id:
        query = query.filter(LabOrder.patient_id == patient_id)
    if status:
        query = query.filter(LabOrder.status == status.upper())
    return query.order_by(LabOrder.order_date.desc()).limit(200).all()


@router.get("/orders/{order_id}", response_model=LabOrderRead)
def get_order(
    order_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    order = db.query(LabOrder).filter(LabOrder.order_id == order_id).first()
    if not order:
        raise ResourceNotFoundError(resource="Lab order")
    return order


@router.post("/orders/{order_id}/results", response_model=LabResultRead, status_code=status.HTTP_201_CREATED)
def add_lab_result(
    order_id: UUID,
    req: LabResultCreate,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(lab_tech_only),
):
    order = db.query(LabOrder).filter(LabOrder.order_id == order_id).first()
    if not order:
        raise ResourceNotFoundError(resource="Lab order")

    result = LabResult(
        **req.model_dump(exclude={"verified_by"}),
        verified_by=current_user.staff_id,
        verified_at=datetime.now(timezone.utc),
    )
    db.add(result)

    item = (
        db.query(LabOrderItem)
        .filter(
            LabOrderItem.order_id == order_id,
            LabOrderItem.test_id == req.test_id,
        )
        .first()
    )
    if item:
        item.status = "COMPLETED"
        item.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(result)

    if result.is_critical:
        notify_critical_lab_result(db, result)

    return result


@router.get("/orders/{order_id}/results", response_model=List[LabResultRead])
def list_results(
    order_id: UUID,
    db: Session = Depends(get_db_with_rls),
    current_user: Staff = Depends(get_current_user),
):
    return db.query(LabResult).filter(LabResult.order_item_id.in_(
        db.query(LabOrderItem.order_item_id).filter(LabOrderItem.order_id == order_id)
    )).all()
