import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Patient, PatientCreate, PatientUpdate, PatientConsent, PatientConsentCreate } from '../models/patient.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PatientService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/patients`;

  create(patient: PatientCreate): Observable<Patient> {
    return this.http.post<Patient>(this.apiUrl, patient);
  }

  list(q?: string): Observable<Patient[]> {
    let params = new HttpParams();
    if (q) params = params.set('q', q);
    return this.http.get<Patient[]>(this.apiUrl, { params });
  }

  get(id: string): Observable<Patient> {
    return this.http.get<Patient>(`${this.apiUrl}/${id}`);
  }

  update(id: string, patient: PatientUpdate): Observable<Patient> {
    return this.http.put<Patient>(`${this.apiUrl}/${id}`, patient);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  addConsent(patientId: string, consent: PatientConsentCreate): Observable<PatientConsent> {
    return this.http.post<PatientConsent>(`${this.apiUrl}/${patientId}/consents`, consent);
  }

  listConsents(patientId: string): Observable<PatientConsent[]> {
    return this.http.get<PatientConsent[]>(`${this.apiUrl}/${patientId}/consents`);
  }
}
