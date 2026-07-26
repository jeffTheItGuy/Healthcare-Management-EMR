export interface Staff {
  staff_id: string;
  staff_number: string;
  national_id: string;
  first_name: string;
  last_name: string;
  role: 'DOCTOR' | 'NURSE' | 'LAB_TECH' | 'PHARMACIST' | 'RADIOLOGIST' | 'ADMIN' | 'CASHIER' | 'MANAGER';
  department_id?: string;
  specialization?: string;
  license_number?: string;
  phone?: string;
  email?: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface PasswordChangeRequest {
  old_password: string;
  new_password: string;
}
