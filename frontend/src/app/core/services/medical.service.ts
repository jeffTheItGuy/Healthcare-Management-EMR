import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MedicalRecord, MedicalRecordCreate, Diagnosis, DiagnosisCreate, Prescription, PrescriptionCreate } from '../models/medical.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class MedicalService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/records`;

  createRecord(record: MedicalRecordCreate): Observable<MedicalRecord> {
    return this.http.post<MedicalRecord>(this.apiUrl, record);
  }

  getRecord(id: string): Observable<MedicalRecord> {
    return this.http.get<MedicalRecord>(`${this.apiUrl}/${id}`);
  }

  addDiagnosis(recordId: string, diagnosis: DiagnosisCreate): Observable<Diagnosis> {
    return this.http.post<Diagnosis>(`${this.apiUrl}/${recordId}/diagnoses`, diagnosis);
  }

  addPrescription(recordId: string, prescription: PrescriptionCreate): Observable<Prescription> {
    return this.http.post<Prescription>(`${this.apiUrl}/${recordId}/prescriptions`, prescription);
  }

  lockRecord(recordId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/${recordId}/lock`, {});
  }
}
