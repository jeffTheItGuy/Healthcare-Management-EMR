export interface Appointment {
  appointment_id: string;
  patient_id: string;
  doctor_id?: string;
  department_id?: string;
  appointment_number: string;
  scheduled_date: string;
  scheduled_time?: string;
  estimated_duration_minutes?: number;
  appointment_type: 'OPD_CONSULTATION' | 'FOLLOW_UP' | 'LAB_REVIEW' | 'PROCEDURE' | 'TELEMEDICINE';
  status: 'SCHEDULED' | 'CHECKED_IN' | 'IN_PROGRESS' | 'COMPLETED' | 'NO_SHOW' | 'CANCELLED';
  chief_complaint?: string;
  notes?: string;
  checked_in_at?: string;
  completed_at?: string;
  created_by?: string;
  created_at: string;
}

export interface AppointmentCreate {
  patient_id: string;
  doctor_id?: string;
  department_id?: string;
  appointment_number: string;
  scheduled_date: string;
  scheduled_time?: string;
  estimated_duration_minutes?: number | null;
  appointment_type: string;
  status?: string;
  chief_complaint?: string;
  notes?: string;
}

export interface AppointmentUpdate {
  doctor_id?: string;
  department_id?: string;
  appointment_number?: string;
  scheduled_date?: string;
  scheduled_time?: string;
  estimated_duration_minutes?: number | null;
  appointment_type?: string;
  status?: string;
  chief_complaint?: string;
  notes?: string;
}