import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  DocumentSearchRequest, DocumentSearchResult,
  PatientSimilarityRequest, PatientSimilarityResult
} from '../models/search.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class SearchService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/search`;

  searchDocuments(req: DocumentSearchRequest): Observable<DocumentSearchResult[]> {
    return this.http.post<DocumentSearchResult[]>(`${this.apiUrl}/documents`, req);
  }

  findSimilarPatients(req: PatientSimilarityRequest): Observable<PatientSimilarityResult[]> {
    return this.http.post<PatientSimilarityResult[]>(`${this.apiUrl}/patients/similar`, req);
  }
}
