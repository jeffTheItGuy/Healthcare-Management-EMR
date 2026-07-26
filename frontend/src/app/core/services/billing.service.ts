import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  MedicalAidProvider, MedicalAidProviderCreate,
  BillingInvoice, BillingInvoiceCreate,
  InvoiceItem, InvoiceItemCreate,
  Payment, PaymentCreate
} from '../models/billing.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class BillingService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/billing`;

  createProvider(provider: MedicalAidProviderCreate): Observable<MedicalAidProvider> {
    return this.http.post<MedicalAidProvider>(`${this.apiUrl}/providers`, provider);
  }

  listProviders(): Observable<MedicalAidProvider[]> {
    return this.http.get<MedicalAidProvider[]>(`${this.apiUrl}/providers`);
  }

  createInvoice(invoice: BillingInvoiceCreate): Observable<BillingInvoice> {
    return this.http.post<BillingInvoice>(`${this.apiUrl}/invoices`, invoice);
  }

  listInvoices(patientId?: string, status?: string): Observable<BillingInvoice[]> {
    let params = new HttpParams();
    if (patientId) params = params.set('patient_id', patientId);
    if (status) params = params.set('status', status);
    return this.http.get<BillingInvoice[]>(`${this.apiUrl}/invoices`, { params });
  }

  getInvoice(id: string): Observable<BillingInvoice> {
    return this.http.get<BillingInvoice>(`${this.apiUrl}/invoices/${id}`);
  }

  addInvoiceItem(invoiceId: string, item: InvoiceItemCreate): Observable<InvoiceItem> {
    return this.http.post<InvoiceItem>(`${this.apiUrl}/invoices/${invoiceId}/items`, item);
  }

  addPayment(invoiceId: string, payment: PaymentCreate): Observable<BillingInvoice> {
    return this.http.post<BillingInvoice>(`${this.apiUrl}/invoices/${invoiceId}/payments`, payment);
  }
}
