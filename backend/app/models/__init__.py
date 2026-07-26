"""SQLAlchemy models for ZimEMR."""
from app.database import Base

from .patient import Patient, PatientConsent, PatientAccessLog
from .staff import Department, Staff, StaffCredential, StaffRoster
from .medical import MedicalRecord, Diagnosis, Prescription, PrescriptionItem
from .admissions import Ward, Bed, Admission
from .lab import LabTestCatalog, LabOrder, LabOrderItem, LabResult
from .pharmacy import Medication, PharmacyInventory, PharmacyBatch, DispensedMedication, Supplier
from .billing import BillingInvoice, InvoiceItem, Payment, MedicalAidProvider
from .audit import AuditLog
from .semantic import ClinicalDocumentSource, ClinicalDocumentChunk, PatientClinicalEmbedding, SearchQuery

__all__ = [
    "Base",
    "Patient", "PatientConsent", "PatientAccessLog",
    "Department", "Staff", "StaffCredential", "StaffRoster",
    "MedicalRecord", "Diagnosis", "Prescription", "PrescriptionItem",
    "Ward", "Bed", "Admission",
    "LabTestCatalog", "LabOrder", "LabOrderItem", "LabResult",
    "Medication", "PharmacyInventory", "PharmacyBatch", "DispensedMedication", "Supplier",
    "BillingInvoice", "InvoiceItem", "Payment", "MedicalAidProvider",
    "AuditLog",
    "ClinicalDocumentSource", "ClinicalDocumentChunk", "PatientClinicalEmbedding", "SearchQuery",
]