import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'login',
    loadChildren: () => import('./features/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'patients',
    canActivate: [authGuard],
    loadChildren: () => import('./features/patients/patients.routes').then(m => m.PATIENT_ROUTES)
  },
  {
    path: 'appointments',
    canActivate: [authGuard],
    loadChildren: () => import('./features/appointments/appointments.routes').then(m => m.APPOINTMENT_ROUTES)
  },
  {
    path: 'clinical',
    canActivate: [authGuard],
    loadChildren: () => import('./features/clinical/clinical.routes').then(m => m.CLINICAL_ROUTES)
  },
  {
    path: 'lab',
    canActivate: [authGuard],
    data: { roles: ['DOCTOR', 'NURSE', 'LAB_TECH', 'ADMIN', 'MANAGER'] },
    canActivateChild: [roleGuard],
    loadChildren: () => import('./features/laboratory/laboratory.routes').then(m => m.LABORATORY_ROUTES)
  },
  {
    path: 'pharmacy',
    canActivate: [authGuard],
    data: { roles: ['PHARMACIST', 'DOCTOR', 'ADMIN', 'MANAGER'] },
    canActivateChild: [roleGuard],
    loadChildren: () => import('./features/pharmacy/pharmacy.routes').then(m => m.PHARMACY_ROUTES)
  },
  {
    path: 'billing',
    canActivate: [authGuard],
    data: { roles: ['CASHIER', 'ADMIN', 'MANAGER'] },
    canActivateChild: [roleGuard],
    loadChildren: () => import('./features/billing/billing.routes').then(m => m.BILLING_ROUTES)
  },
  {
    path: 'staff',
    canActivate: [authGuard],
    data: { roles: ['ADMIN', 'MANAGER'] },
    canActivateChild: [roleGuard],
    loadChildren: () => import('./features/staff/staff.routes').then(m => m.STAFF_ROUTES)
  },
  {
    path: 'search',
    canActivate: [authGuard],
    loadChildren: () => import('./features/search/search.routes').then(m => m.SEARCH_ROUTES)
  },
  { path: '**', redirectTo: 'dashboard' }
];
