import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Medication, MedicationCreate,
  PharmacyInventory, PharmacyInventoryCreate,
  PharmacyBatch, PharmacyBatchCreate,
  Supplier, SupplierCreate,
  DispensedMedication, DispensedMedicationCreate
} from '../models/pharmacy.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PharmacyService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/pharmacy`;

  createMedication(med: MedicationCreate): Observable<Medication> {
    return this.http.post<Medication>(`${this.apiUrl}/medications`, med);
  }

  listMedications(): Observable<Medication[]> {
    return this.http.get<Medication[]>(`${this.apiUrl}/medications`);
  }

  createInventory(inv: PharmacyInventoryCreate): Observable<PharmacyInventory> {
    return this.http.post<PharmacyInventory>(`${this.apiUrl}/inventory`, inv);
  }

  listInventory(): Observable<PharmacyInventory[]> {
    return this.http.get<PharmacyInventory[]>(`${this.apiUrl}/inventory`);
  }

  createSupplier(supplier: SupplierCreate): Observable<Supplier> {
    return this.http.post<Supplier>(`${this.apiUrl}/suppliers`, supplier);
  }

  listSuppliers(): Observable<Supplier[]> {
    return this.http.get<Supplier[]>(`${this.apiUrl}/suppliers`);
  }

  createBatch(batch: PharmacyBatchCreate): Observable<PharmacyBatch> {
    return this.http.post<PharmacyBatch>(`${this.apiUrl}/batches`, batch);
  }

  listBatches(medicationId?: string): Observable<PharmacyBatch[]> {
    let params = new HttpParams();
    if (medicationId) params = params.set('medication_id', medicationId);
    return this.http.get<PharmacyBatch[]>(`${this.apiUrl}/batches`, { params });
  }

  dispense(dispense: DispensedMedicationCreate): Observable<DispensedMedication> {
    return this.http.post<DispensedMedication>(`${this.apiUrl}/dispense`, dispense);
  }
}
