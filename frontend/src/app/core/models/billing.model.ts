export interface MedicalAidProvider {
  provider_id: string;
  provider_code: string;
  provider_name: string;
  contact_phone?: string;
  contact_email?: string;
  claim_submission_url?: string;
  is_active: boolean;
  created_at: string;
}

export interface MedicalAidProviderCreate {
  provider_code: string;
  provider_name: string;
  contact_phone?: string;
  contact_email?: string;
  claim_submission_url?: string;
  is_active?: boolean;
}

export interface BillingInvoice {
  invoice_id: string;
  invoice_number: string;
  patient_id: string;
  record_id?: string;
  admission_id?: string;
  invoice_type: string;
  currency_code: string;
  exchange_rate: string;
  subtotal: string;
  discount_amount: string;
  tax_amount: string;
  total_amount: string;
  base_currency_total: string;
  amount_paid: string;
  balance_due: string;
  payment_status: 'UNPAID' | 'PARTIAL' | 'PAID' | 'OVERPAID' | 'WRITTEN_OFF';
  medical_aid_claimed: boolean;
  medical_aid_claim_amount?: string;
  medical_aid_claim_reference?: string;
  invoice_date: string;
  due_date?: string;
  created_by?: string;
  created_at: string;
}

export interface BillingInvoiceCreate {
  invoice_number: string;
  patient_id: string;
  record_id?: string;
  admission_id?: string;
  invoice_type: string;
  currency_code?: string;
  exchange_rate?: string;
  subtotal?: string;
  discount_amount?: string;
  tax_amount?: string;
  total_amount?: string;
  base_currency_total?: string;
  amount_paid?: string;
  balance_due?: string;
  payment_status?: string;
  medical_aid_claimed?: boolean;
  medical_aid_claim_amount?: string;
  medical_aid_claim_reference?: string;
  due_date?: string;
}

export interface InvoiceItem {
  item_id: string;
  invoice_id: string;
  item_type: 'CONSULTATION' | 'PROCEDURE' | 'MEDICATION' | 'LAB_TEST' | 'WARD_CHARGE' | 'THEATRE' | 'SUPPLY' | 'PACKAGE';
  reference_id?: string;
  description?: string;
  quantity?: string;
  unit_price?: string;
  currency_code: string;
  line_total?: string;
  base_currency_line_total?: string;
  created_at: string;
}

export interface InvoiceItemCreate {
  invoice_id: string;
  item_type: string;
  reference_id?: string;
  description?: string;
  quantity?: string;
  unit_price?: string;
  currency_code?: string;
  line_total?: string;
  base_currency_line_total?: string;
}

export interface Payment {
  payment_id: string;
  invoice_id: string;
  patient_id: string;
  payment_method: 'CASH' | 'CARD' | 'BANK_TRANSFER' | 'MOBILE_MONEY' | 'INSURANCE' | 'MEDICAL_AID';
  currency_code: string;
  amount: string;
  exchange_rate: string;
  base_currency_amount?: string;
  reference_number?: string;
  received_by?: string;
  payment_date: string;
  reconciled: boolean;
  created_at: string;
}

export interface PaymentCreate {
  invoice_id: string;
  patient_id: string;
  payment_method: string;
  currency_code?: string;
  amount: string;
  exchange_rate?: string;
  base_currency_amount?: string;
  reference_number?: string;
  received_by?: string;
}
