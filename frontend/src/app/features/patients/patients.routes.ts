import { Routes } from '@angular/router';

export const PATIENT_ROUTES: Routes = [
  { path: '', loadComponent: () => import('./pages/list/list.component').then(m => m.ListComponent) },
  { path: 'new', loadComponent: () => import('./pages/form/form.component').then(m => m.FormComponent) },
  { path: ':id', loadComponent: () => import('./pages/detail/detail.component').then(m => m.DetailComponent) },
  { path: ':id/edit', loadComponent: () => import('./pages/form/form.component').then(m => m.FormComponent) }
];
