export interface Medication {
  medication_id: string;
  generic_name: string;
  brand_name?: string;
  dosage_form: 'TABLET' | 'CAPSULE' | 'SYRUP' | 'INJECTION' | 'CREAM' | 'DROPS' | 'INHALER' | 'SUPPOSITORY';
  strength?: string;
  atc_code?: string;
  category?: string;
  reorder_level?: string;
  reorder_quantity?: string;
  is_controlled: boolean;
  schedule?: string;
  is_active: boolean;
  created_at: string;
}

export interface MedicationCreate {
  generic_name: string;
  brand_name?: string;
  dosage_form: string;
  strength?: string;
  atc_code?: string;
  category?: string;
  reorder_level?: string;
  reorder_quantity?: string;
  is_controlled?: boolean;
  schedule?: string;
  is_active?: boolean;
}

export interface PharmacyInventory {
  inventory_id: string;
  medication_id: string;
  total_quantity: string;
  available_quantity: string;
  reserved_quantity: string;
  unit_cost_average?: string;
  currency_code: string;
  location_rack?: string;
  is_active: boolean;
  updated_at: string;
}

export interface PharmacyInventoryCreate {
  medication_id: string;
  total_quantity?: string;
  available_quantity?: string;
  reserved_quantity?: string;
  unit_cost_average?: string;
  currency_code?: string;
  location_rack?: string;
  is_active?: boolean;
}

export interface Supplier {
  supplier_id: string;
  supplier_code: string;
  supplier_name: string;
  contact_person?: string;
  phone?: string;
  email?: string;
  address?: string;
  license_number?: string;
  is_active: boolean;
  created_at: string;
}

export interface SupplierCreate {
  supplier_code: string;
  supplier_name: string;
  contact_person?: string;
  phone?: string;
  email?: string;
  address?: string;
  license_number?: string;
  is_active?: boolean;
}

export interface PharmacyBatch {
  batch_id: string;
  inventory_id?: string;
  medication_id: string;
  batch_number: string;
  supplier_id?: string;
  quantity_received?: string;
  quantity_remaining?: string;
  unit_cost?: string;
  currency_code: string;
  expiry_date?: string;
  manufacturing_date?: string;
  received_date?: string;
  grn_reference?: string;
  status: string;
  created_at: string;
}

export interface PharmacyBatchCreate {
  inventory_id?: string;
  medication_id: string;
  batch_number: string;
  supplier_id?: string;
  quantity_received?: string;
  quantity_remaining?: string;
  unit_cost?: string;
  currency_code?: string;
  expiry_date?: string;
  manufacturing_date?: string;
  received_date?: string;
  grn_reference?: string;
  status?: string;
}

export interface DispensedMedication {
  dispense_id: string;
  prescription_item_id: string;
  batch_id?: string;
  patient_id: string;
  dispensed_by: string;
  quantity_dispensed?: string;
  unit_price?: string;
  currency_code: string;
  total_amount?: string;
  dispense_date: string;
  created_at: string;
}

export interface DispensedMedicationCreate {
  prescription_item_id: string;
  batch_id?: string;
  patient_id: string;
  dispensed_by: string;
  quantity_dispensed?: string;
  unit_price?: string;
  currency_code?: string;
  total_amount?: string;
}
