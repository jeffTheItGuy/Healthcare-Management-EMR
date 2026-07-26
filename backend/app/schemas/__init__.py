"""Pydantic schemas for request/response validation."""

from .patient import PatientBase, PatientCreate, PatientRead, PatientUpdate, PatientConsentBase, PatientConsentCreate, PatientConsentRead
from .staff import DepartmentBase, DepartmentCreate, DepartmentRead, StaffBase, StaffCreate, StaffRead, StaffCredentialBase, StaffCredentialCreate, StaffRosterBase, StaffRosterCreate, StaffRosterRead
from .medical import MedicalRecordBase, MedicalRecordCreate, MedicalRecordRead, DiagnosisBase, DiagnosisCreate, PrescriptionBase, PrescriptionCreate, PrescriptionItemBase, PrescriptionItemCreate
from .admissions import WardBase, WardCreate, WardRead, BedBase, BedCreate, BedRead, AdmissionBase, AdmissionCreate, AdmissionRead, AdmissionUpdate
from .lab import LabTestCatalogBase, LabTestCatalogCreate, LabTestCatalogRead, LabOrderBase, LabOrderCreate, LabOrderRead, LabOrderItemBase, LabOrderItemCreate, LabResultBase, LabResultCreate, LabResultRead
from .pharmacy import MedicationBase, MedicationCreate, MedicationRead, PharmacyInventoryBase, PharmacyInventoryCreate, PharmacyBatchBase, PharmacyBatchCreate, DispensedMedicationBase, DispensedMedicationCreate, SupplierBase, SupplierCreate, SupplierRead
from .billing import MedicalAidProviderBase, MedicalAidProviderCreate, MedicalAidProviderRead, BillingInvoiceBase, BillingInvoiceCreate, BillingInvoiceRead, InvoiceItemBase, InvoiceItemCreate, PaymentBase, PaymentCreate, PaymentRead
from .search import DocumentSearchRequest, DocumentSearchResult, PatientSimilarityRequest, PatientSimilarityResult

__all__ = [
    "PatientBase", "PatientCreate", "PatientRead", "PatientUpdate", "PatientConsentBase", "PatientConsentCreate", "PatientConsentRead",
    "DepartmentBase", "DepartmentCreate", "DepartmentRead", "StaffBase", "StaffCreate", "StaffRead", "StaffCredentialBase", "StaffCredentialCreate", "StaffRosterBase", "StaffRosterCreate", "StaffRosterRead",
    "MedicalRecordBase", "MedicalRecordCreate", "MedicalRecordRead", "DiagnosisBase", "DiagnosisCreate", "PrescriptionBase", "PrescriptionCreate", "PrescriptionItemBase", "PrescriptionItemCreate",
    "WardBase", "WardCreate", "WardRead", "BedBase", "BedCreate", "BedRead", "AdmissionBase", "AdmissionCreate", "AdmissionRead", "AdmissionUpdate",
    "LabTestCatalogBase", "LabTestCatalogCreate", "LabTestCatalogRead", "LabOrderBase", "LabOrderCreate", "LabOrderRead", "LabOrderItemBase", "LabOrderItemCreate", "LabResultBase", "LabResultCreate", "LabResultRead",
    "MedicationBase", "MedicationCreate", "MedicationRead", "PharmacyInventoryBase", "PharmacyInventoryCreate", "PharmacyBatchBase", "PharmacyBatchCreate", "DispensedMedicationBase", "DispensedMedicationCreate", "SupplierBase", "SupplierCreate", "SupplierRead",
    "MedicalAidProviderBase", "MedicalAidProviderCreate", "MedicalAidProviderRead", "BillingInvoiceBase", "BillingInvoiceCreate", "BillingInvoiceRead", "InvoiceItemBase", "InvoiceItemCreate", "PaymentBase", "PaymentCreate", "PaymentRead",
    "DocumentSearchRequest", "DocumentSearchResult", "PatientSimilarityRequest", "PatientSimilarityResult",
]