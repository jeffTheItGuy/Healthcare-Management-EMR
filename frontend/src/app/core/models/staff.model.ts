export interface Department {
  department_id: string;
  department_code: string;
  department_name: string;
  department_type: string;
  location?: string;
  is_active: boolean;
  created_at: string;
}

export interface DepartmentCreate {
  department_code: string;
  department_name: string;
  department_type: string;
  location?: string;
  is_active?: boolean;
}

export interface Staff {
  staff_id: string;
  staff_number: string;
  national_id: string;
  first_name: string;
  last_name: string;
  role: string;
  department_id?: string;
  specialization?: string;
  license_number?: string;
  phone?: string;
  email?: string;
  is_active: boolean;
  created_at: string;
}

export interface StaffCreate {
  staff_number: string;
  national_id: string;
  first_name: string;
  last_name: string;
  role: string;
  department_id?: string;
  specialization?: string;
  license_number?: string;
  phone?: string;
  email?: string;
  is_active?: boolean;
  password: string;
}

export interface StaffCredential {
  credential_id: string;
  staff_id: string;
  username: string;
  mfa_enabled: boolean;
  last_login_at?: string;
  password_changed_at?: string;
  failed_login_attempts?: string;
  locked_until?: string;
  created_at: string;
}

export interface StaffRoster {
  roster_id: string;
  staff_id: string;
  department_id?: string;
  roster_date: string;
  shift_type: string;
  start_time?: string;
  end_time?: string;
  ward_id?: string;
  notes?: string;
  created_by?: string;
  created_at: string;
}

export interface StaffRosterCreate {
  staff_id: string;
  department_id?: string;
  roster_date: string;
  shift_type: string;
  start_time?: string;
  end_time?: string;
  ward_id?: string;
  notes?: string;
}
