import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { Staff, LoginRequest, LoginResponse, PasswordChangeRequest } from '../models/auth.model';
import { environment } from '../../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private apiUrl = `${environment.apiUrl}/auth`;

  private currentUserSubject = new BehaviorSubject<Staff | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  get currentUserValue(): Staff | null {
    return this.currentUserSubject.value;
  }

  constructor() {
    const token = this.getToken();
    if (token) {
      this.me().subscribe({ error: () => this.logout() });
    }
  }

  login(req: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, req).pipe(
      tap(res => {
        localStorage.setItem('access_token', res.access_token);
        this.me().subscribe();
      })
    );
  }

  me(): Observable<Staff> {
    return this.http.get<Staff>(`${this.apiUrl}/me`).pipe(
      tap(user => this.currentUserSubject.next(user))
    );
  }

  changePassword(req: PasswordChangeRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/change-password`, req);
  }

  logout(): void {
    localStorage.removeItem('access_token');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  hasRole(role: string): boolean {
    return this.currentUserValue?.role === role;
  }

  hasAnyRole(roles: string[]): boolean {
    return !!this.currentUserValue && roles.includes(this.currentUserValue.role);
  }
}
