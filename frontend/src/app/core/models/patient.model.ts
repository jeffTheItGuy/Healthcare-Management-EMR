export interface Patient {
  patient_id: string;
  patient_number: string;
  national_id?: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'MALE' | 'FEMALE' | 'OTHER';
  blood_group?: string;
  phone_primary?: string;
  phone_secondary?: string;
  email?: string;
  address?: string;
  city?: string;
  suburb?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  medical_aid_provider_id?: string;
  medical_aid_number?: string;
  medical_aid_plan?: string;
  allergies?: string;
  chronic_conditions?: string;
  is_active: boolean;
  deleted_at?: string;
  created_at: string;
  updated_at?: string;
}

export interface PatientCreate {
  patient_number: string;
  national_id?: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: 'MALE' | 'FEMALE' | 'OTHER';
  blood_group?: string;
  phone_primary?: string;
  phone_secondary?: string;
  email?: string;
  address?: string;
  city?: string;
  suburb?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  medical_aid_provider_id?: string;
  medical_aid_number?: string;
  medical_aid_plan?: string;
  allergies?: string;
  chronic_conditions?: string;
  is_active?: boolean;
}

export interface PatientUpdate {
  first_name?: string;
  last_name?: string;
  phone_primary?: string;
  phone_secondary?: string;
  email?: string;
  address?: string;
  city?: string;
  suburb?: string;
  emergency_contact_name?: string;
  emergency_contact_phone?: string;
  medical_aid_provider_id?: string;
  medical_aid_number?: string;
  medical_aid_plan?: string;
  allergies?: string;
  chronic_conditions?: string;
  is_active?: boolean;
}

export interface PatientConsent {
  consent_id: string;
  patient_id: string;
  consent_type: 'TREATMENT' | 'DATA_SHARING' | 'RESEARCH' | 'MARKETING';
  consent_given: boolean;
  consent_document?: string;
  valid_from: string;
  valid_until?: string;
  revoked_at?: string;
  created_at: string;
}

export interface PatientConsentCreate {
  patient_id: string;
  consent_type: string;
  consent_given: boolean;
  consent_document?: string;
  valid_from: string;
  valid_until?: string;
}
