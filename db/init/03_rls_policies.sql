ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE medical_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE patient_clinical_embeddings ENABLE ROW LEVEL SECURITY;

CREATE ROLE emr_staff;
CREATE ROLE emr_admin;

CREATE POLICY staff_own_department ON patients
    FOR ALL
    TO emr_staff
    USING (
        patient_id IN (
            SELECT DISTINCT patient_id FROM medical_records
            WHERE attending_doctor_id = current_setting('app.current_staff_id')::UUID
            OR nurse_id = current_setting('app.current_staff_id')::UUID
        )
        OR patient_id IN (
            SELECT DISTINCT p.patient_id FROM patients p
            JOIN appointments a ON p.patient_id = a.patient_id
            JOIN staff s ON a.department_id = s.department_id
            WHERE s.staff_id = current_setting('app.current_staff_id')::UUID
        )
    );

CREATE POLICY patient_self_access ON patients
    FOR SELECT
    TO PUBLIC
    USING (patient_id = current_setting('app.current_patient_id')::UUID);

CREATE POLICY staff_own_records ON medical_records
    FOR ALL
    TO emr_staff
    USING (
        patient_id IN (
            SELECT patient_id FROM patients
            WHERE patient_id = medical_records.patient_id
        )
    );

CREATE POLICY staff_own_embeddings ON patient_clinical_embeddings
    FOR ALL
    TO emr_staff
    USING (
        patient_id IN (
            SELECT patient_id FROM patients
            WHERE patient_id = patient_clinical_embeddings.patient_id
        )
    );

CREATE POLICY admin_all ON patients FOR ALL TO emr_admin USING (true);
CREATE POLICY admin_all_records ON medical_records FOR ALL TO emr_admin USING (true);
CREATE POLICY admin_all_embeddings ON patient_clinical_embeddings FOR ALL TO emr_admin USING (true);