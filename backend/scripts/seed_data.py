#!/usr/bin/env python3
"""
Database Seeder
Usage:
    docker compose -f docker-compose.dev.yml exec backend python scripts/seed_data.py
"""
import sys
import os
from datetime import date, datetime, timezone, timedelta
from uuid import uuid4

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.staff import Department, Staff, StaffCredential
from app.models.patient import Patient, PatientConsent
from app.models.admissions import Ward, Bed, Admission
from app.models.appointments import Appointment
from app.models.medical import MedicalRecord, Diagnosis, Prescription
from app.models.lab import LabTestCatalog, LabOrder, LabOrderItem
from app.models.pharmacy import Medication, PharmacyInventory, Supplier, PharmacyBatch
from app.models.billing import MedicalAidProvider, BillingInvoice, InvoiceItem
from app.core.security import get_password_hash


def seed_departments(db: Session):
    if db.query(Department).first():
        print("  Departments already seeded.")
        return

    depts = [
        Department(department_code="EMRG", department_name="Emergency", department_type="OPD", location="Ground Floor", is_active=True),
        Department(department_code="OPD",  department_name="Outpatients", department_type="OPD", location="1st Floor", is_active=True),
        Department(department_code="LAB",  department_name="Laboratory", department_type="LABORATORY", location="1st Floor", is_active=True),
        Department(department_code="PHARM", department_name="Pharmacy", department_type="PHARMACY", location="Ground Floor", is_active=True),
        Department(department_code="MAT",  department_name="Maternity", department_type="IPD", location="2nd Floor", is_active=True),
        Department(department_code="ICU",  department_name="Intensive Care", department_type="IPD", location="2nd Floor", is_active=True),
        Department(department_code="ADMIN", department_name="Administration", department_type="ADMIN", location="1st Floor", is_active=True),
        Department(department_code="FIN",  department_name="Finance", department_type="FINANCE", location="1st Floor", is_active=True),
    ]
    db.add_all(depts)
    db.commit()
    print(f"  Seeded {len(depts)} departments.")


def seed_medical_aid_providers(db: Session):
    if db.query(MedicalAidProvider).first():
        print("  Medical aid providers already seeded.")
        return

    providers = [
        MedicalAidProvider(
            provider_code="PROV_A",
            provider_name="PROV_A Medical Aid",
            contact_phone="0242-308500",
            contact_email="claims@provider-a.example.com",
            is_active=True,
        ),
        MedicalAidProvider(
            provider_code="PROV_B",
            provider_name="PROV_B",
            contact_phone="0242-700011",
            contact_email="claims@provider-b.example.com",
            is_active=True,
        ),
    ]
    db.add_all(providers)
    db.commit()
    print(f"  Seeded {len(providers)} medical aid providers.")


def seed_staff(db: Session):
    if db.query(Staff).first():
        print("  Staff already seeded.")
        return

    admin_dept = db.query(Department).filter_by(department_code="ADMIN").first()
    emrg_dept  = db.query(Department).filter_by(department_code="EMRG").first()
    lab_dept   = db.query(Department).filter_by(department_code="LAB").first()
    pharm_dept = db.query(Department).filter_by(department_code="PHARM").first()

    staff_list = [
        Staff(
            staff_number="S-ADMIN-001",
            national_id="63-0000001-A-00",
            first_name="System",
            last_name="Administrator",
            role="ADMIN",
            department_id=admin_dept.department_id,
            email="admin@example.com",
            is_active=True,
        ),
        Staff(
            staff_number="S-DOC-001",
            national_id="63-1234567-A-12",
            first_name="Tendai",
            last_name="Moyo",
            role="DOCTOR",
            department_id=emrg_dept.department_id,
            specialization="Emergency Medicine",
            license_number="MDZ-2015-0042",
            phone="0772123456",
            email="t.moyo@example.com",
            is_active=True,
        ),
        Staff(
            staff_number="S-NUR-001",
            national_id="63-7654321-B-34",
            first_name="Grace",
            last_name="Mutasa",
            role="NURSE",
            department_id=emrg_dept.department_id,
            license_number="RNZ-2018-0091",
            phone="0772987654",
            email="g.mutasa@example.com",
            is_active=True,
        ),
        Staff(
            staff_number="S-LAB-001",
            national_id="63-1111111-C-56",
            first_name="Peter",
            last_name="Chiwara",
            role="LAB_TECH",
            department_id=lab_dept.department_id,
            license_number="LTZ-2020-0012",
            phone="0773123456",
            is_active=True,
        ),
        Staff(
            staff_number="S-PHARM-001",
            national_id="63-2222222-D-78",
            first_name="Rudo",
            last_name="Kaseke",
            role="PHARMACIST",
            department_id=pharm_dept.department_id,
            license_number="PHZ-2019-0034",
            phone="0774567890",
            is_active=True,
        ),
        Staff(
            staff_number="S-CASH-001",
            national_id="63-3333333-E-90",
            first_name="Blessing",
            last_name="Ncube",
            role="CASHIER",
            department_id=admin_dept.department_id,
            phone="0775123456",
            is_active=True,
        ),
    ]
    db.add_all(staff_list)
    db.flush()

    creds = [
        StaffCredential(staff_id=staff_list[0].staff_id, username="admin", password_hash=get_password_hash("admin123")),
        StaffCredential(staff_id=staff_list[1].staff_id, username="tdmoyo", password_hash=get_password_hash("doctor123")),
        StaffCredential(staff_id=staff_list[2].staff_id, username="gmutasa", password_hash=get_password_hash("nurse123")),
        StaffCredential(staff_id=staff_list[3].staff_id, username="pchiwara", password_hash=get_password_hash("lab123")),
        StaffCredential(staff_id=staff_list[4].staff_id, username="rkaseke", password_hash=get_password_hash("pharm123")),
        StaffCredential(staff_id=staff_list[5].staff_id, username="bncube", password_hash=get_password_hash("cash123")),
    ]
    db.add_all(creds)
    db.commit()
    print(f"  Seeded {len(staff_list)} staff members with credentials.")
    print("    Login: admin / admin123")


def seed_wards_and_beds(db: Session):
    if db.query(Ward).first():
        print("  Wards already seeded.")
        return

    emrg = db.query(Department).filter_by(department_code="EMRG").first()
    mat  = db.query(Department).filter_by(department_code="MAT").first()
    icu  = db.query(Department).filter_by(department_code="ICU").first()

    wards = [
        Ward(ward_code="GEN-A", ward_name="General Ward A", department_id=emrg.department_id, ward_type="GENERAL", floor_level=1, capacity=10, is_active=True),
        Ward(ward_code="ICU-1", ward_name="ICU", department_id=icu.department_id, ward_type="ICU", floor_level=2, capacity=4, is_active=True),
        Ward(ward_code="MAT-1", ward_name="Maternity Ward", department_id=mat.department_id, ward_type="MATERNITY", floor_level=2, capacity=6, is_active=True),
    ]
    db.add_all(wards)
    db.flush()

    beds = []
    for w in wards:
        count = int(w.capacity)
        for i in range(1, count + 1):
            bed_type = "STANDARD"
            if w.ward_type == "ICU":
                bed_type = "ELECTRIC"
            elif w.ward_type == "MATERNITY":
                bed_type = "BASSINET" if i <= 3 else "STANDARD"
            beds.append(Bed(ward_id=w.ward_id, bed_number=f"{w.ward_code}-{i:02d}", bed_type=bed_type, status="AVAILABLE"))
    db.add_all(beds)
    db.commit()
    print(f"  Seeded {len(wards)} wards and {len(beds)} beds.")


def seed_medications(db: Session):
    if db.query(Medication).first():
        print("  Medications already seeded.")
        return

    meds = [
        Medication(generic_name="Paracetamol", brand_name="Panadol", dosage_form="TABLET", strength="500mg", category="Analgesic", reorder_level=100, reorder_quantity=500, is_active=True),
        Medication(generic_name="Amoxicillin", brand_name="Amoxil", dosage_form="CAPSULE", strength="250mg", category="Antibiotic", reorder_level=50, reorder_quantity=300, is_active=True),
        Medication(generic_name="Metformin", brand_name="Glucophage", dosage_form="TABLET", strength="500mg", category="Antidiabetic", reorder_level=60, reorder_quantity=200, is_active=True),
        Medication(generic_name="Artemether/Lumefantrine", brand_name="Coartem", dosage_form="TABLET", strength="20/120mg", category="Antimalarial", reorder_level=80, reorder_quantity=400, is_active=True),
        Medication(generic_name="Ibuprofen", brand_name="Brufen", dosage_form="TABLET", strength="400mg", category="NSAID", reorder_level=40, reorder_quantity=200, is_active=True),
    ]
    db.add_all(meds)
    db.flush()

    invs = []
    for m in meds:
        invs.append(PharmacyInventory(
            medication_id=m.medication_id,
            total_quantity=1000,
            available_quantity=1000,
            reserved_quantity=0,
            unit_cost_average=2.50,
            currency_code="USD",
            location_rack="A-01",
            is_active=True,
        ))
    db.add_all(invs)

    supplier = Supplier(supplier_code="SUP-001", supplier_name="Generic Pharmaceuticals", contact_person="Mr. Patel", phone="0242-123456", is_active=True)
    db.add(supplier)
    db.flush()

    batches = []
    for i, m in enumerate(meds):
        batches.append(PharmacyBatch(
            inventory_id=invs[i].inventory_id,
            medication_id=m.medication_id,
            batch_number=f"BATCH-2024-{i+1:03d}",
            supplier_id=supplier.supplier_id,
            quantity_received=1000,
            quantity_remaining=1000,
            unit_cost=2.50,
            currency_code="USD",
            expiry_date=date(2026, 12, 31),
            received_date=date(2024, 1, 15),
            status="ACTIVE",
        ))
    db.add_all(batches)
    db.commit()
    print(f"  Seeded {len(meds)} medications with inventory and batches.")


def seed_lab_catalog(db: Session):
    if db.query(LabTestCatalog).first():
        print("  Lab catalog already seeded.")
        return

    tests = [
        LabTestCatalog(test_code="FBC", test_name="Full Blood Count", category="Hematology", sample_type="EDTA Blood", turnaround_hours=2, base_price=15.00, currency_code="USD", is_active=True),
        LabTestCatalog(test_code="MAL-RDT", test_name="Malaria Rapid Diagnostic Test", category="Microbiology", sample_type="Capillary Blood", turnaround_hours=1, base_price=5.00, currency_code="USD", is_active=True),
        LabTestCatalog(test_code="RBS", test_name="Random Blood Glucose", category="Biochemistry", sample_type="Fluoride Plasma", turnaround_hours=1, base_price=8.00, currency_code="USD", is_active=True),
        LabTestCatalog(test_code="HIV-RDT", test_name="HIV Rapid Test", category="Serology", sample_type="Capillary Blood", turnaround_hours=1, base_price=6.00, currency_code="USD", is_active=True),
        LabTestCatalog(test_code="URINE", test_name="Urinalysis", category="Microscopy", sample_type="Urine", turnaround_hours=2, base_price=7.00, currency_code="USD", is_active=True),
        LabTestCatalog(test_code="TB-GENE", test_name="TB GeneXpert", category="Molecular", sample_type="Sputum", turnaround_hours=24, base_price=45.00, currency_code="USD", is_active=True),
    ]
    db.add_all(tests)
    db.commit()
    print(f"  Seeded {len(tests)} lab tests.")


def seed_patients(db: Session):
    if db.query(Patient).first():
        print("  Patients already seeded.")
        return

    cimas = db.query(MedicalAidProvider).filter_by(provider_code="PROV_A").first()

    patients = [
        Patient(
            patient_number="P-2024-000001",
            national_id="63-1111111-A-11",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1985, 5, 15),
            gender="MALE",
            blood_group="O+",
            phone_primary="0771234567",
            phone_secondary="0712345678",
            email="john.doe@example.com",
            address="12 Main Street",
            city="City A",
            suburb="Suburb A",
            emergency_contact_name="Jane Doe",
            emergency_contact_phone="0779876543",
            medical_aid_provider_id=cimas.provider_id if cimas else None,
            medical_aid_number="PROV_A-001234",
            allergies="Penicillin",
            is_active=True,
        ),
        Patient(
            patient_number="P-2024-000002",
            national_id="63-2222222-B-22",
            first_name="Sarah",
            last_name="Mupfumi",
            date_of_birth=date(1992, 8, 22),
            gender="FEMALE",
            blood_group="A+",
            phone_primary="0774567890",
            city="City B",
            suburb="Suburb B",
            emergency_contact_name="Tendai Mupfumi",
            emergency_contact_phone="0771122334",
            is_active=True,
        ),
        Patient(
            patient_number="P-2024-000003",
            national_id="63-3333333-C-33",
            first_name="Tatenda",
            last_name="Chikwava",
            date_of_birth=date(1978, 3, 10),
            gender="MALE",
            phone_primary="0775566778",
            city="City A",
            suburb="Suburb C",
            chronic_conditions="Hypertension, Type 2 Diabetes",
            is_active=True,
        ),
    ]
    db.add_all(patients)
    db.flush()

    consent = PatientConsent(
        patient_id=patients[0].patient_id,
        consent_type="TREATMENT",
        consent_given=True,
        valid_from=date(2024, 1, 1),
    )
    db.add(consent)
    db.commit()
    print(f"  Seeded {len(patients)} patients.")


def seed_appointments_and_records(db: Session):
    if db.query(Appointment).first():
        print("  Appointments already seeded.")
        return

    patient = db.query(Patient).filter_by(patient_number="P-2024-000001").first()
    doctor = db.query(Staff).filter_by(staff_number="S-DOC-001").first()
    nurse  = db.query(Staff).filter_by(staff_number="S-NUR-001").first()

    if not all([patient, doctor, nurse]):
        print("  Skipping appointments (missing patient or staff).")
        return

    appt = Appointment(
        patient_id=patient.patient_id,
        doctor_id=doctor.staff_id,
        appointment_number="APT-2024-0001",
        scheduled_date=date.today() + timedelta(days=1),
        scheduled_time=datetime.now(timezone.utc).time(),
        appointment_type="OPD_CONSULTATION",
        status="SCHEDULED",
        notes="Follow-up for hypertension",
    )
    db.add(appt)
    db.flush()

    record = MedicalRecord(
        patient_id=patient.patient_id,
        appointment_id=appt.appointment_id,
        encounter_type="OPD",
        attending_doctor_id=doctor.staff_id,
        nurse_id=nurse.staff_id,
        chief_complaint="Headache and dizziness for 3 days",
        history_of_present_illness="Patient reports gradual onset of frontal headache, worse in mornings. No fever.",
        physical_examination="BP 160/100 mmHg, HR 88 bpm, Temp 36.7°C",
        vital_signs={"temperature": "36.7", "blood_pressure": "160/100", "pulse": "88", "respiratory_rate": "18", "spo2": "98"},
        assessment_and_plan="Hypertension - uncontrolled. Increase amlodipine to 10mg daily. Review in 2 weeks.",
    )
    db.add(record)
    db.flush()

    diag = Diagnosis(
        record_id=record.record_id,
        icd10_code="I10",
        diagnosis_name="Essential Hypertension",
        diagnosis_type="PRIMARY",
        notes="Uncontrolled on current regimen",
        diagnosed_by=doctor.staff_id,
    )
    db.add(diag)

    rx = Prescription(
        record_id=record.record_id,
        patient_id=patient.patient_id,
        prescribed_by=doctor.staff_id,
        status="PENDING",
    )
    db.add(rx)
    db.commit()
    print("  Seeded appointments, medical records, diagnosis, and prescription.")


def seed_admissions(db: Session):
    if db.query(Admission).first():
        print("  Admissions already seeded.")
        return

    patient = db.query(Patient).filter_by(patient_number="P-2024-000003").first()
    doctor = db.query(Staff).filter_by(staff_number="S-DOC-001").first()
    bed = db.query(Bed).filter_by(bed_number="ICU-1-01").first()

    if not all([patient, doctor, bed]):
        print("  Skipping admissions (missing dependencies).")
        return

    adm = Admission(
        patient_id=patient.patient_id,
        bed_id=bed.bed_id,
        admitting_doctor_id=doctor.staff_id,
        admission_number="ADM-2024-0001",
        admission_type="EMERGENCY",
        status="ADMITTED",
    )
    db.add(adm)
    db.flush()

    bed.status = "OCCUPIED"
    bed.current_admission_id = adm.admission_id
    db.commit()
    print("  Seeded 1 admission and occupied ICU bed.")


def seed_lab_orders(db: Session):
    if db.query(LabOrder).first():
        print("  Lab orders already seeded.")
        return

    patient = db.query(Patient).filter_by(patient_number="P-2024-000001").first()
    doctor = db.query(Staff).filter_by(staff_number="S-DOC-001").first()
    fbc = db.query(LabTestCatalog).filter_by(test_code="FBC").first()
    rbs = db.query(LabTestCatalog).filter_by(test_code="RBS").first()

    if not all([patient, doctor, fbc, rbs]):
        print("  Skipping lab orders (missing dependencies).")
        return

    order = LabOrder(
        order_number="LAB-2024-0001",
        patient_id=patient.patient_id,
        ordered_by=doctor.staff_id,
        priority="ROUTINE",
        status="ORDERED",
        clinical_notes="Pre-op baseline",
    )
    db.add(order)
    db.flush()

    item1 = LabOrderItem(order_id=order.order_id, test_id=fbc.test_id, status="PENDING")
    item2 = LabOrderItem(order_id=order.order_id, test_id=rbs.test_id, status="PENDING")
    db.add_all([item1, item2])
    db.commit()
    print("  Seeded 1 lab order with 2 items.")


def seed_billing(db: Session):
    if db.query(BillingInvoice).first():
        print("  Billing already seeded.")
        return

    patient = db.query(Patient).filter_by(patient_number="P-2024-000001").first()
    cashier = db.query(Staff).filter_by(staff_number="S-CASH-001").first()

    if not all([patient, cashier]):
        print("  Skipping billing (missing dependencies).")
        return

    inv = BillingInvoice(
        invoice_number="INV-2024-0001",
        patient_id=patient.patient_id,
        invoice_type="OPD",
        currency_code="USD",
        exchange_rate=1.0,
        subtotal=30.00,
        discount_amount=0,
        tax_amount=0,
        total_amount=30.00,
        base_currency_total=30.00,
        amount_paid=0,
        balance_due=30.00,
        payment_status="UNPAID",
    )
    db.add(inv)
    db.flush()

    item = InvoiceItem(
        invoice_id=inv.invoice_id,
        item_type="CONSULTATION",
        description="OPD Consultation - Dr. Moyo",
        quantity=1,
        unit_price=15.00,
        currency_code="USD",
        line_total=15.00,
        base_currency_line_total=15.00,
    )
    db.add(item)

    item2 = InvoiceItem(
        invoice_id=inv.invoice_id,
        item_type="LAB_TEST",
        description="Full Blood Count",
        quantity=1,
        unit_price=15.00,
        currency_code="USD",
        line_total=15.00,
        base_currency_line_total=15.00,
    )
    db.add(item2)
    db.commit()
    print("  Seeded 1 invoice with 2 line items.")


def main():
    print("🌱 Seeding database...")
    db = SessionLocal()
    try:
        seed_departments(db)
        seed_medical_aid_providers(db)
        seed_staff(db)
        seed_wards_and_beds(db)
        seed_medications(db)
        seed_lab_catalog(db)
        seed_patients(db)
        seed_appointments_and_records(db)
        seed_admissions(db)
        seed_lab_orders(db)
        seed_billing(db)
        print("✅ Seed complete!")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()