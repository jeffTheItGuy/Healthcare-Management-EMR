import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ward, WardCreate, Bed, BedCreate, Admission, AdmissionCreate, AdmissionUpdate } from '../models/admissions.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AdmissionsService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/admissions`;

  createWard(ward: WardCreate): Observable<Ward> {
    return this.http.post<Ward>(`${this.apiUrl}/wards`, ward);
  }

  listWards(): Observable<Ward[]> {
    return this.http.get<Ward[]>(`${this.apiUrl}/wards`);
  }

  createBed(wardId: string, bed: BedCreate): Observable<Bed> {
    return this.http.post<Bed>(`${this.apiUrl}/wards/${wardId}/beds`, bed);
  }

  listBeds(wardId: string, status?: string): Observable<Bed[]> {
    let params = new HttpParams();
    if (status) params = params.set('status', status);
    return this.http.get<Bed[]>(`${this.apiUrl}/wards/${wardId}/beds`, { params });
  }

  admit(admission: AdmissionCreate): Observable<Admission> {
    return this.http.post<Admission>(this.apiUrl, admission);
  }

  listAdmissions(patientId?: string, status?: string): Observable<Admission[]> {
    let params = new HttpParams();
    if (patientId) params = params.set('patient_id', patientId);
    if (status) params = params.set('status', status);
    return this.http.get<Admission[]>(this.apiUrl, { params });
  }

  getAdmission(id: string): Observable<Admission> {
    return this.http.get<Admission>(`${this.apiUrl}/${id}`);
  }

  discharge(id: string, update: AdmissionUpdate): Observable<Admission> {
    return this.http.post<Admission>(`${this.apiUrl}/${id}/discharge`, update);
  }
}
