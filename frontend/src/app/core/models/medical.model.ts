export interface MedicalRecord {
  record_id: string;
  patient_id: string;
  appointment_id?: string;
  admission_id?: string;
  encounter_type: 'OPD' | 'IPD' | 'EMERGENCY' | 'TELEMEDICINE';
  attending_doctor_id?: string;
  nurse_id?: string;
  encounter_date: string;
  chief_complaint?: string;
  history_of_present_illness?: string;
  physical_examination?: string;
  vital_signs?: Record<string, any>;
  assessment_and_plan?: string;
  discharge_notes?: string;
  follow_up_instructions?: string;
  is_locked: boolean;
  locked_by?: string;
  locked_at?: string;
  created_at: string;
}

export interface MedicalRecordCreate {
  patient_id: string;
  appointment_id?: string;
  admission_id?: string;
  encounter_type: string;
  attending_doctor_id?: string;
  nurse_id?: string;
  chief_complaint?: string;
  history_of_present_illness?: string;
  physical_examination?: string;
  vital_signs?: Record<string, any>;
  assessment_and_plan?: string;
  discharge_notes?: string;
  follow_up_instructions?: string;
}

export interface Diagnosis {
  diagnosis_id: string;
  record_id: string;
  icd10_code?: string;
  diagnosis_name: string;
  diagnosis_type: 'PRIMARY' | 'SECONDARY' | 'DIFFERENTIAL';
  notes?: string;
  diagnosed_by?: string;
  created_at: string;
}

export interface DiagnosisCreate {
  record_id: string;
  icd10_code?: string;
  diagnosis_name: string;
  diagnosis_type: string;
  notes?: string;
}

export interface Prescription {
  prescription_id: string;
  record_id: string;
  patient_id: string;
  prescribed_by: string;
  prescription_date: string;
  status: 'PENDING' | 'DISPENSED' | 'PARTIAL' | 'CANCELLED';
  pharmacy_notes?: string;
  created_at: string;
}

export interface PrescriptionCreate {
  record_id: string;
  patient_id: string;
  prescribed_by: string;
  status?: string;
  pharmacy_notes?: string;
}

export interface PrescriptionItem {
  item_id: string;
  prescription_id: string;
  medication_id: string;
  dosage?: string;
  frequency?: string;
  duration_days?: number;
  quantity_prescribed?: string;
  quantity_dispensed?: string;
  instructions?: string;
  is_substitutable: boolean;
  created_at: string;
}

export interface PrescriptionItemCreate {
  prescription_id: string;
  medication_id: string;
  dosage?: string;
  frequency?: string;
  duration_days?: number;
  quantity_prescribed?: string;
  quantity_dispensed?: string;
  instructions?: string;
  is_substitutable?: boolean;
}
