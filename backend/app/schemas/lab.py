from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class LabTestCatalogBase(BaseModel):
    test_code: str
    test_name: str
    category: Optional[str] = None
    description: Optional[str] = None
    sample_type: Optional[str] = None
    turnaround_hours: Optional[str] = None
    normal_range: Optional[str] = None
    unit_of_measure: Optional[str] = None
    base_price: Optional[str] = None
    currency_code: str = "USD"
    is_active: bool = True


class LabTestCatalogCreate(LabTestCatalogBase):
    pass


class LabTestCatalogRead(LabTestCatalogBase):
    model_config = ConfigDict(from_attributes=True)

    test_id: UUID
    created_at: datetime


class LabOrderBase(BaseModel):
    order_number: str
    patient_id: UUID
    record_id: Optional[UUID] = None
    ordered_by: Optional[UUID] = None
    priority: str = "ROUTINE"
    status: str = "ORDERED"
    clinical_notes: Optional[str] = None


class LabOrderCreate(LabOrderBase):
    pass


class LabOrderRead(LabOrderBase):
    model_config = ConfigDict(from_attributes=True)

    order_id: UUID
    order_date: datetime
    created_at: datetime


class LabOrderItemBase(BaseModel):
    order_id: UUID
    test_id: UUID
    status: str = "PENDING"


class LabOrderItemCreate(LabOrderItemBase):
    pass


class LabResultBase(BaseModel):
    order_item_id: UUID
    test_id: UUID
    patient_id: UUID
    result_value: Optional[str] = None
    result_numeric: Optional[str] = None
    unit_of_measure: Optional[str] = None
    reference_range: Optional[str] = None
    interpretation: Optional[str] = None
    verified_by: Optional[UUID] = None
    result_notes: Optional[str] = None
    is_critical: bool = False


class LabResultCreate(LabResultBase):
    pass


class LabResultRead(LabResultBase):
    model_config = ConfigDict(from_attributes=True)

    result_id: UUID
    verified_at: Optional[datetime] = None
    critical_notified_at: Optional[datetime] = None
    created_at: datetime