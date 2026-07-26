-- B-TREE
CREATE INDEX idx_patients_number ON patients(patient_number);
CREATE INDEX idx_patients_national_id ON patients(national_id);
CREATE INDEX idx_appointments_patient_date ON appointments(patient_id, scheduled_date, status);
CREATE INDEX idx_appointments_doctor_date ON appointments(doctor_id, scheduled_date);
CREATE INDEX idx_medical_records_patient_date ON medical_records(patient_id, encounter_date);
CREATE INDEX idx_prescriptions_patient_status ON prescriptions(patient_id, status);
CREATE INDEX idx_pharmacy_batches_med_status_expiry ON pharmacy_batches(medication_id, status, expiry_date);
CREATE INDEX idx_pharmacy_batches_expiry_active ON pharmacy_batches(expiry_date, status) WHERE status = 'ACTIVE';
CREATE INDEX idx_dispensed_patient_date ON dispensed_medications(patient_id, dispense_date);
CREATE INDEX idx_lab_orders_patient_status_date ON lab_orders(patient_id, status, order_date);
CREATE INDEX idx_lab_results_patient_test_date ON lab_results(patient_id, test_id, created_at);
CREATE INDEX idx_billing_patient_status_date ON billing_invoices(patient_id, payment_status, invoice_date);
CREATE INDEX idx_billing_invoice_number ON billing_invoices(invoice_number);
CREATE INDEX idx_invoice_items_invoice_type ON invoice_items(invoice_id, item_type);
CREATE INDEX idx_payments_invoice_date ON payments(invoice_id, payment_date);
CREATE INDEX idx_staff_rosters_staff_date ON staff_rosters(staff_id, roster_date);
CREATE INDEX idx_admissions_patient_status_date ON admissions(patient_id, status, admission_date);

-- HNSW (pgvector)
CREATE INDEX idx_document_chunks_hnsw
ON clinical_document_chunks
USING hnsw (chunk_text_embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE INDEX idx_patient_embeddings_hnsw
ON patient_clinical_embeddings
USING hnsw (embedding_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);