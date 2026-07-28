-- ============================================================
-- ZIMBABWE HOSPITAL EMR — CORE SCHEMA
-- Run after 01_extensions.sql
-- ============================================================

-- ===== MEDICAL AID =====
CREATE TABLE medical_aid_providers (
    provider_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider_code VARCHAR(20) UNIQUE NOT NULL,
    provider_name VARCHAR(200) NOT NULL,
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    claim_submission_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== DEPARTMENTS =====
CREATE TABLE departments (
    department_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    department_code VARCHAR(20) UNIQUE NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    department_type VARCHAR(50) NOT NULL CHECK (department_type IN ('OPD','IPD','LABORATORY','PHARMACY','RADIOLOGY','ADMIN','FINANCE','THEATRE')),
    location VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== STAFF =====
CREATE TABLE staff (
    staff_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    staff_number VARCHAR(20) UNIQUE NOT NULL,
    national_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('DOCTOR','NURSE','LAB_TECH','PHARMACIST','RADIOLOGIST','ADMIN','CASHIER','MANAGER')),
    department_id UUID REFERENCES departments(department_id),
    specialization VARCHAR(100),
    license_number VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE staff_credentials (
    credential_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    staff_id UUID REFERENCES staff(staff_id) ON DELETE CASCADE,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    last_login_at TIMESTAMPTZ,
    password_changed_at TIMESTAMPTZ,
    failed_login_attempts INT DEFAULT 0,
    locked_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== WARDS & BEDS =====
CREATE TABLE wards (
    ward_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ward_code VARCHAR(20) UNIQUE NOT NULL,
    ward_name VARCHAR(100) NOT NULL,
    department_id UUID REFERENCES departments(department_id),
    ward_type VARCHAR(50) NOT NULL CHECK (ward_type IN ('GENERAL','PRIVATE','ICU','MATERNITY','PAEDIATRIC','ISOLATION')),
    floor_level INT,
    capacity INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE beds (
    bed_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ward_id UUID REFERENCES wards(ward_id),
    bed_number VARCHAR(20) NOT NULL,
    bed_type VARCHAR(50) NOT NULL CHECK (bed_type IN ('STANDARD','ELECTRIC','BASSINET','ISOLATION')),
    status VARCHAR(20) DEFAULT 'AVAILABLE' CHECK (status IN ('AVAILABLE','OCCUPIED','MAINTENANCE','RESERVED')),
    current_admission_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ward_id, bed_number)
);

-- ===== PATIENTS =====
CREATE TABLE patients (
    patient_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_number VARCHAR(20) UNIQUE NOT NULL,
    national_id VARCHAR(50),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('MALE','FEMALE','OTHER')),
    blood_group VARCHAR(5),
    phone_primary VARCHAR(20),
    phone_secondary VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    suburb VARCHAR(100),
    emergency_contact_name VARCHAR(200),
    emergency_contact_phone VARCHAR(20),
    medical_aid_provider_id UUID REFERENCES medical_aid_providers(provider_id),
    medical_aid_number VARCHAR(50),
    medical_aid_plan VARCHAR(50),
    allergies TEXT,
    chronic_conditions TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    deleted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE patient_consents (
    consent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id) ON DELETE CASCADE,
    consent_type VARCHAR(50) NOT NULL CHECK (consent_type IN ('TREATMENT','DATA_SHARING','RESEARCH','MARKETING')),
    consent_given BOOLEAN NOT NULL,
    consent_document VARCHAR(500),
    valid_from DATE NOT NULL,
    valid_until DATE,
    revoked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE patient_access_logs (
    access_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    accessed_by_staff_id UUID REFERENCES staff(staff_id),
    access_reason VARCHAR(255),
    access_type VARCHAR(20) NOT NULL CHECK (access_type IN ('VIEW','CREATE','UPDATE','DELETE','EXPORT')),
    ip_address INET,
    accessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== APPOINTMENTS =====
CREATE TABLE appointments (
    appointment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    appointment_number VARCHAR(20) UNIQUE NOT NULL,
    patient_id UUID REFERENCES patients(patient_id),
    doctor_id UUID REFERENCES staff(staff_id),
    department_id UUID REFERENCES departments(department_id),
    appointment_type VARCHAR(50) NOT NULL CHECK (appointment_type IN ('OPD_CONSULTATION','FOLLOW_UP','LAB_REVIEW','PROCEDURE','TELEMEDICINE')),
    scheduled_date DATE NOT NULL,
    scheduled_time TIME,
    estimated_duration_minutes INT,
    status VARCHAR(20) DEFAULT 'SCHEDULED' CHECK (status IN ('SCHEDULED','CHECKED_IN','IN_PROGRESS','COMPLETED','NO_SHOW','CANCELLED')),
    chief_complaint TEXT,
    notes TEXT,
    checked_in_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== MEDICAL RECORDS =====
CREATE TABLE medical_records (
    record_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    appointment_id UUID REFERENCES appointments(appointment_id),
    admission_id UUID,
    encounter_type VARCHAR(20) NOT NULL CHECK (encounter_type IN ('OPD','IPD','EMERGENCY','TELEMEDICINE')),
    attending_doctor_id UUID REFERENCES staff(staff_id),
    nurse_id UUID REFERENCES staff(staff_id),
    encounter_date TIMESTAMPTZ DEFAULT NOW(),
    chief_complaint TEXT,
    history_of_present_illness TEXT,
    physical_examination TEXT,
    vital_signs JSONB,
    assessment_and_plan TEXT,
    discharge_notes TEXT,
    follow_up_instructions TEXT,
    is_locked BOOLEAN DEFAULT FALSE,
    locked_by UUID,
    locked_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE diagnoses (
    diagnosis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    record_id UUID REFERENCES medical_records(record_id),
    icd10_code VARCHAR(10),
    diagnosis_name VARCHAR(255) NOT NULL,
    diagnosis_type VARCHAR(20) NOT NULL CHECK (diagnosis_type IN ('PRIMARY','SECONDARY','DIFFERENTIAL')),
    notes TEXT,
    diagnosed_by UUID REFERENCES staff(staff_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== PRESCRIPTIONS =====
CREATE TABLE prescriptions (
    prescription_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    record_id UUID REFERENCES medical_records(record_id),
    patient_id UUID REFERENCES patients(patient_id),
    prescribed_by UUID REFERENCES staff(staff_id),
    prescription_date TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING','DISPENSED','PARTIAL','CANCELLED')),
    pharmacy_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== MEDICATIONS =====
CREATE TABLE medications (
    medication_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    generic_name VARCHAR(255) NOT NULL,
    brand_name VARCHAR(255),
    dosage_form VARCHAR(50) NOT NULL CHECK (dosage_form IN ('TABLET','CAPSULE','SYRUP','INJECTION','CREAM','DROPS','INHALER','SUPPOSITORY')),
    strength VARCHAR(50),
    atc_code VARCHAR(10),
    category VARCHAR(100),
    reorder_level INT,
    reorder_quantity INT,
    is_controlled BOOLEAN DEFAULT FALSE,
    schedule VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE prescription_items (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prescription_id UUID REFERENCES prescriptions(prescription_id),
    medication_id UUID REFERENCES medications(medication_id),
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    duration_days INT,
    quantity_prescribed DECIMAL(10,2),
    quantity_dispensed DECIMAL(10,2),
    instructions TEXT,
    is_substitutable BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== ADMISSIONS =====
CREATE TABLE admissions (
    admission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    bed_id UUID REFERENCES beds(bed_id),
    admitting_doctor_id UUID REFERENCES staff(staff_id),
    admission_number VARCHAR(20) UNIQUE NOT NULL,
    admission_type VARCHAR(20) NOT NULL CHECK (admission_type IN ('ELECTIVE','EMERGENCY','REFERRAL')),
    admission_date TIMESTAMPTZ DEFAULT NOW(),
    discharge_date TIMESTAMPTZ,
    discharge_type VARCHAR(20) CHECK (discharge_type IN ('HOME','TRANSFER','DEATH','ABSCONDED')),
    discharge_summary TEXT,
    status VARCHAR(20) DEFAULT 'ADMITTED' CHECK (status IN ('ADMITTED','DISCHARGED','TRANSFERRED')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== LAB =====
CREATE TABLE lab_test_catalog (
    test_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_code VARCHAR(20) UNIQUE NOT NULL,
    test_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    sample_type VARCHAR(50),
    turnaround_hours INT,
    normal_range TEXT,
    unit_of_measure VARCHAR(20),
    base_price DECIMAL(18,2),
    currency_code CHAR(3) DEFAULT 'USD',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE lab_orders (
    order_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_number VARCHAR(20) UNIQUE NOT NULL,
    patient_id UUID REFERENCES patients(patient_id),
    record_id UUID REFERENCES medical_records(record_id),
    ordered_by UUID REFERENCES staff(staff_id),
    order_date TIMESTAMPTZ DEFAULT NOW(),
    priority VARCHAR(20) DEFAULT 'ROUTINE' CHECK (priority IN ('ROUTINE','URGENT','STAT')),
    status VARCHAR(20) DEFAULT 'ORDERED' CHECK (status IN ('ORDERED','SAMPLE_COLLECTED','IN_PROGRESS','COMPLETED','CANCELLED')),
    clinical_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE lab_order_items (
    order_item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES lab_orders(order_id),
    test_id UUID REFERENCES lab_test_catalog(test_id),
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING','IN_PROGRESS','COMPLETED','CANCELLED')),
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE lab_results (
    result_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_item_id UUID REFERENCES lab_order_items(order_item_id),
    test_id UUID REFERENCES lab_test_catalog(test_id),
    patient_id UUID REFERENCES patients(patient_id),
    result_value VARCHAR(255),
    result_numeric DECIMAL(18,6),
    unit_of_measure VARCHAR(20),
    reference_range TEXT,
    interpretation VARCHAR(20) CHECK (interpretation IN ('NORMAL','ABNORMAL','CRITICAL','BORDERLINE')),
    verified_by UUID REFERENCES staff(staff_id),
    verified_at TIMESTAMPTZ,
    result_notes TEXT,
    is_critical BOOLEAN DEFAULT FALSE,
    critical_notified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== PHARMACY INVENTORY =====
CREATE TABLE pharmacy_inventory (
    inventory_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    medication_id UUID REFERENCES medications(medication_id),
    total_quantity INT DEFAULT 0,
    available_quantity INT DEFAULT 0,
    reserved_quantity INT DEFAULT 0,
    unit_cost_average DECIMAL(18,4),
    currency_code CHAR(3) DEFAULT 'USD',
    location_rack VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE suppliers (
    supplier_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    supplier_code VARCHAR(20) UNIQUE NOT NULL,
    supplier_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    license_number VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pharmacy_batches (
    batch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    inventory_id UUID REFERENCES pharmacy_inventory(inventory_id),
    medication_id UUID REFERENCES medications(medication_id),
    batch_number VARCHAR(50) NOT NULL,
    supplier_id UUID REFERENCES suppliers(supplier_id),
    quantity_received INT,
    quantity_remaining INT,
    unit_cost DECIMAL(18,4),
    currency_code CHAR(3) DEFAULT 'USD',
    expiry_date DATE,
    manufacturing_date DATE,
    received_date DATE,
    grn_reference VARCHAR(50),
    status VARCHAR(20) DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE','EXPIRED','DEPLETED','QUARANTINE')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(medication_id, batch_number)
);

CREATE TABLE dispensed_medications (
    dispense_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prescription_item_id UUID REFERENCES prescription_items(item_id),
    batch_id UUID REFERENCES pharmacy_batches(batch_id),
    patient_id UUID REFERENCES patients(patient_id),
    dispensed_by UUID REFERENCES staff(staff_id),
    quantity_dispensed INT,
    unit_price DECIMAL(18,4),
    currency_code CHAR(3) DEFAULT 'USD',
    total_amount DECIMAL(18,2),
    dispense_date TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== BILLING =====
CREATE TABLE billing_invoices (
    invoice_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    patient_id UUID REFERENCES patients(patient_id),
    record_id UUID REFERENCES medical_records(record_id),
    admission_id UUID REFERENCES admissions(admission_id),
    invoice_type VARCHAR(20) NOT NULL CHECK (invoice_type IN ('OPD','IPD','PHARMACY','LABORATORY','PACKAGE','MIXED')),
    currency_code CHAR(3) DEFAULT 'USD',
    exchange_rate DECIMAL(24,10) DEFAULT 1.0,
    subtotal DECIMAL(18,2) DEFAULT 0,
    discount_amount DECIMAL(18,2) DEFAULT 0,
    tax_amount DECIMAL(18,2) DEFAULT 0,
    total_amount DECIMAL(18,2) DEFAULT 0,
    base_currency_total DECIMAL(18,2) DEFAULT 0,
    amount_paid DECIMAL(18,2) DEFAULT 0,
    balance_due DECIMAL(18,2) DEFAULT 0,
    payment_status VARCHAR(20) DEFAULT 'UNPAID' CHECK (payment_status IN ('UNPAID','PARTIAL','PAID','OVERPAID','WRITTEN_OFF')),
    medical_aid_claimed BOOLEAN DEFAULT FALSE,
    medical_aid_claim_amount DECIMAL(18,2),
    medical_aid_claim_reference VARCHAR(50),
    invoice_date TIMESTAMPTZ DEFAULT NOW(),
    due_date DATE,
    created_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE invoice_items (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES billing_invoices(invoice_id),
    item_type VARCHAR(50) NOT NULL CHECK (item_type IN ('CONSULTATION','PROCEDURE','MEDICATION','LAB_TEST','WARD_CHARGE','THEATRE','SUPPLY','PACKAGE')),
    reference_id UUID,
    description TEXT,
    quantity DECIMAL(10,2),
    unit_price DECIMAL(18,4),
    currency_code CHAR(3) DEFAULT 'USD',
    line_total DECIMAL(18,2),
    base_currency_line_total DECIMAL(18,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE payments (
    payment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES billing_invoices(invoice_id),
    patient_id UUID REFERENCES patients(patient_id),
    payment_method VARCHAR(50) NOT NULL CHECK (payment_method IN ('CASH','ECOCASH','ZIPIT','BANK_TRANSFER','CARD','USD_CASH','ZiG_CASH','MEDICAL_AID')),
    currency_code CHAR(3) DEFAULT 'USD',
    amount DECIMAL(18,2) NOT NULL,
    exchange_rate DECIMAL(24,10) DEFAULT 1.0,
    base_currency_amount DECIMAL(18,2),
    reference_number VARCHAR(100),
    received_by UUID REFERENCES staff(staff_id),
    payment_date TIMESTAMPTZ DEFAULT NOW(),
    reconciled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== AUDIT =====
CREATE TABLE audit_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id UUID,
    staff_id UUID,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== SEMANTIC SEARCH (pgvector) =====
CREATE TABLE clinical_document_sources (
    source_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_title VARCHAR(500) NOT NULL,
    source_type VARCHAR(50) NOT NULL CHECK (source_type IN ('GUIDELINE','PROTOCOL','RESEARCH_PAPER','DRUG_REFERENCE','SOP','TEXTBOOK')),
    document_url VARCHAR(1000),
    file_hash VARCHAR(64),
    page_count INT,
    language VARCHAR(10) DEFAULT 'en',
    specialty_tags TEXT[],
    ingest_status VARCHAR(20) DEFAULT 'PENDING',
    is_active BOOLEAN DEFAULT TRUE,
    ingested_by UUID REFERENCES staff(staff_id),
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE clinical_document_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES clinical_document_sources(source_id),
    chunk_index INT NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_text_embedding VECTOR(384),
    chunk_metadata JSONB,
    token_count INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE patient_clinical_embeddings (
    embedding_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID REFERENCES patients(patient_id),
    record_id UUID REFERENCES medical_records(record_id),
    embedding_type VARCHAR(50) NOT NULL CHECK (embedding_type IN ('RECORD_SUMMARY','CHIEF_COMPLAINT','DIAGNOSIS_HISTORY','FULL_HISTORY')),
    embedding_text TEXT NOT NULL,
    embedding_vector VECTOR(384),
    model_name VARCHAR(50),
    model_version VARCHAR(20),
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(patient_id, record_id, embedding_type)
);

CREATE TABLE search_queries (
    query_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    queried_by_staff_id UUID REFERENCES staff(staff_id),
    query_text TEXT NOT NULL,
    query_embedding VECTOR(384),
    search_target VARCHAR(20) DEFAULT 'DOCUMENTS' CHECK (search_target IN ('PATIENTS','DOCUMENTS','ALL')),
    filters JSONB,
    top_k INT DEFAULT 10,
    similarity_threshold DECIMAL(3,2) DEFAULT 0.70,
    results JSONB,
    result_count INT,
    execution_time_ms INT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ===== STAFF ROSTERS =====
CREATE TABLE staff_rosters (
    roster_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    staff_id UUID REFERENCES staff(staff_id) NOT NULL,
    department_id UUID REFERENCES departments(department_id),
    roster_date DATE NOT NULL,
    shift_type VARCHAR(20) NOT NULL,
    start_time VARCHAR(8),
    end_time VARCHAR(8),
    ward_id UUID REFERENCES wards(ward_id),
    notes TEXT,
    created_by UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(staff_id, roster_date, shift_type)
);