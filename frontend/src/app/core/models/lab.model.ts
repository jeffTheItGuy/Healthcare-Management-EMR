export interface LabTestCatalog {
  test_id: string;
  test_code: string;
  test_name: string;
  category?: string;
  description?: string;
  sample_type?: string;
  turnaround_hours?: string;
  normal_range?: string;
  unit_of_measure?: string;
  base_price?: string;
  currency_code: string;
  is_active: boolean;
  created_at: string;
}

export interface LabTestCatalogCreate {
  test_code: string;
  test_name: string;
  category?: string;
  description?: string;
  sample_type?: string;
  turnaround_hours?: string;
  normal_range?: string;
  unit_of_measure?: string;
  base_price?: string;
  currency_code?: string;
  is_active?: boolean;
}

export interface LabOrder {
  order_id: string;
  order_number: string;
  patient_id: string;
  record_id?: string;
  ordered_by: string;
  order_date: string;
  priority: string;
  status: string;
  clinical_notes?: string;
  created_at: string;
}

export interface LabOrderCreate {
  order_number: string;
  patient_id: string;
  record_id?: string;
  priority?: string;
  status?: string;
  clinical_notes?: string;
}

export interface LabOrderItem {
  order_item_id: string;
  order_id: string;
  test_id: string;
  status: string;
  completed_at?: string;
  created_at: string;
}

export interface LabOrderItemCreate {
  order_id: string;
  test_id: string;
  status?: string;
}

export interface LabResult {
  result_id: string;
  order_item_id: string;
  test_id: string;
  patient_id: string;
  result_value?: string;
  result_numeric?: string;
  unit_of_measure?: string;
  reference_range?: string;
  interpretation?: 'NORMAL' | 'ABNORMAL' | 'CRITICAL' | 'BORDERLINE';
  verified_by?: string;
  verified_at?: string;
  result_notes?: string;
  is_critical: boolean;
  critical_notified_at?: string;
  created_at: string;
}

export interface LabResultCreate {
  order_item_id: string;
  test_id: string;
  patient_id: string;
  result_value?: string;
  result_numeric?: string;
  unit_of_measure?: string;
  reference_range?: string;
  interpretation?: string;
  result_notes?: string;
  is_critical?: boolean;
}
