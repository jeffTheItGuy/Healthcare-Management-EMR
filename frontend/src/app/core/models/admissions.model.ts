export interface Ward {
  ward_id: string;
  ward_code: string;
  ward_name: string;
  department_id?: string;
  ward_type: 'GENERAL' | 'PRIVATE' | 'ICU' | 'MATERNITY' | 'PAEDIATRIC' | 'ISOLATION';
  floor_level?: string;
  capacity?: string;
  is_active: boolean;
  created_at: string;
}

export interface WardCreate {
  ward_code: string;
  ward_name: string;
  department_id?: string;
  ward_type: string;
  floor_level?: string;
  capacity?: string;
  is_active?: boolean;
}

export interface Bed {
  bed_id: string;
  ward_id: string;
  bed_number: string;
  bed_type: 'STANDARD' | 'ELECTRIC' | 'BASSINET' | 'ISOLATION';
  status: 'AVAILABLE' | 'OCCUPIED' | 'MAINTENANCE' | 'RESERVED';
  current_admission_id?: string;
  created_at: string;
}

export interface BedCreate {
  ward_id: string;
  bed_number: string;
  bed_type: string;
  status?: string;
  current_admission_id?: string;
}

export interface Admission {
  admission_id: string;
  patient_id: string;
  bed_id?: string;
  admitting_doctor_id?: string;
  admission_number: string;
  admission_type: 'ELECTIVE' | 'EMERGENCY' | 'REFERRAL';
  admission_date: string;
  discharge_date?: string;
  discharge_type?: 'HOME' | 'TRANSFER' | 'DEATH' | 'ABSCONDED';
  discharge_summary?: string;
  status: 'ADMITTED' | 'DISCHARGED' | 'TRANSFERRED';
  created_at: string;
}

export interface AdmissionCreate {
  patient_id: string;
  bed_id?: string;
  admission_number: string;
  admission_type: string;
  discharge_date?: string;
  discharge_type?: string;
  discharge_summary?: string;
  status?: string;
}

export interface AdmissionUpdate {
  bed_id?: string;
  discharge_date?: string;
  discharge_type?: string;
  discharge_summary?: string;
  status?: string;
}
