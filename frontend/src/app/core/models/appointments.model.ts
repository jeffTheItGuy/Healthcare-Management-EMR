export interface Appointment {
  appointment_id: string;
  patient_id: string;
  staff_id?: string;
  appointment_date: string;
  appointment_type: 'OPD_CONSULTATION' | 'FOLLOW_UP' | 'LAB_REVIEW' | 'PROCEDURE' | 'TELEMEDICINE';
  status: 'SCHEDULED' | 'CHECKED_IN' | 'IN_PROGRESS' | 'COMPLETED' | 'NO_SHOW' | 'CANCELLED';
  notes?: string;
  created_at: string;
}

export interface AppointmentCreate {
  patient_id: string;
  staff_id?: string;
  appointment_date: string;
  appointment_type: string;
  status?: string;
  notes?: string;
}

export interface AppointmentUpdate {
  staff_id?: string;
  appointment_date?: string;
  appointment_type?: string;
  status?: string;
  notes?: string;
}
