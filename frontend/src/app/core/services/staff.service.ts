import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Department, DepartmentCreate, Staff, StaffCreate, StaffRoster, StaffRosterCreate } from '../models/staff.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class StaffService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/staff`;

  createDepartment(dept: DepartmentCreate): Observable<Department> {
    return this.http.post<Department>(`${this.apiUrl}/departments`, dept);
  }

  listDepartments(): Observable<Department[]> {
    return this.http.get<Department[]>(`${this.apiUrl}/departments`);
  }

  createStaff(staff: StaffCreate): Observable<Staff> {
    return this.http.post<Staff>(this.apiUrl, staff);
  }

  listStaff(departmentId?: string, role?: string): Observable<Staff[]> {
    let params = new HttpParams();
    if (departmentId) params = params.set('department_id', departmentId);
    if (role) params = params.set('role', role);
    return this.http.get<Staff[]>(this.apiUrl, { params });
  }

  getStaff(id: string): Observable<Staff> {
    return this.http.get<Staff>(`${this.apiUrl}/${id}`);
  }

  addRoster(staffId: string, roster: StaffRosterCreate): Observable<StaffRoster> {
    return this.http.post<StaffRoster>(`${this.apiUrl}/${staffId}/roster`, roster);
  }

  getRoster(staffId: string): Observable<StaffRoster[]> {
    return this.http.get<StaffRoster[]>(`${this.apiUrl}/${staffId}/roster`);
  }
}
