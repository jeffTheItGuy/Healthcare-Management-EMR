import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LabTestCatalog, LabTestCatalogCreate, LabOrder, LabOrderCreate, LabResult, LabResultCreate } from '../models/lab.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class LabService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/lab`;

  createTestCatalog(test: LabTestCatalogCreate): Observable<LabTestCatalog> {
    return this.http.post<LabTestCatalog>(`${this.apiUrl}/catalog`, test);
  }

  listCatalog(category?: string): Observable<LabTestCatalog[]> {
    let params = new HttpParams();
    if (category) params = params.set('category', category);
    return this.http.get<LabTestCatalog[]>(`${this.apiUrl}/catalog`, { params });
  }

  createOrder(order: LabOrderCreate): Observable<LabOrder> {
    return this.http.post<LabOrder>(`${this.apiUrl}/orders`, order);
  }

  listOrders(patientId?: string, status?: string): Observable<LabOrder[]> {
    let params = new HttpParams();
    if (patientId) params = params.set('patient_id', patientId);
    if (status) params = params.set('status', status);
    return this.http.get<LabOrder[]>(`${this.apiUrl}/orders`, { params });
  }

  getOrder(id: string): Observable<LabOrder> {
    return this.http.get<LabOrder>(`${this.apiUrl}/orders/${id}`);
  }

  addResult(orderId: string, result: LabResultCreate): Observable<LabResult> {
    return this.http.post<LabResult>(`${this.apiUrl}/orders/${orderId}/results`, result);
  }

  listResults(orderId: string): Observable<LabResult[]> {
    return this.http.get<LabResult[]>(`${this.apiUrl}/orders/${orderId}/results`);
  }
}
