from datetime import date, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class MedicationBase(BaseModel):
    generic_name: str
    brand_name: Optional[str] = None
    dosage_form: str
    strength: Optional[str] = None
    atc_code: Optional[str] = None
    category: Optional[str] = None
    reorder_level: Optional[str] = None
    reorder_quantity: Optional[str] = None
    is_controlled: bool = False
    schedule: Optional[str] = None
    is_active: bool = True


class MedicationCreate(MedicationBase):
    pass


class MedicationRead(MedicationBase):
    model_config = ConfigDict(from_attributes=True)

    medication_id: UUID
    created_at: datetime


class PharmacyInventoryBase(BaseModel):
    medication_id: UUID
    total_quantity: str = "0"
    available_quantity: str = "0"
    reserved_quantity: str = "0"
    unit_cost_average: Optional[str] = None
    currency_code: str = "USD"
    location_rack: Optional[str] = None
    is_active: bool = True


class PharmacyInventoryCreate(PharmacyInventoryBase):
    pass


class PharmacyBatchBase(BaseModel):
    inventory_id: Optional[UUID] = None
    medication_id: UUID
    batch_number: str
    supplier_id: Optional[UUID] = None
    quantity_received: Optional[str] = None
    quantity_remaining: Optional[str] = None
    unit_cost: Optional[str] = None
    currency_code: str = "USD"
    expiry_date: Optional[date] = None
    manufacturing_date: Optional[date] = None
    received_date: Optional[date] = None
    grn_reference: Optional[str] = None
    status: str = "ACTIVE"


class PharmacyBatchCreate(PharmacyBatchBase):
    pass


class DispensedMedicationBase(BaseModel):
    prescription_item_id: UUID
    batch_id: Optional[UUID] = None
    patient_id: UUID
    dispensed_by: UUID
    quantity_dispensed: Optional[str] = None
    unit_price: Optional[str] = None
    currency_code: str = "USD"
    total_amount: Optional[str] = None


class DispensedMedicationCreate(DispensedMedicationBase):
    pass


class SupplierBase(BaseModel):
    supplier_code: str
    supplier_name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    license_number: Optional[str] = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    pass


class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: UUID
    created_at: datetime