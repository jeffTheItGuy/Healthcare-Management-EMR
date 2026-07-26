import { Routes } from '@angular/router';

export const CLINICAL_ROUTES: Routes = [
  { path: '', redirectTo: 'records', pathMatch: 'full' },
  { path: 'records', loadComponent: () => import('./pages/records/records.component').then(m => m.RecordsComponent) },
  { path: 'records/:id', loadComponent: () => import('./pages/record-detail/record-detail.component').then(m => m.RecordDetailComponent) },
  { path: 'records/:id/edit', loadComponent: () => import('./pages/record-editor/record-editor.component').then(m => m.RecordEditorComponent) },
  { path: 'ward-map', loadComponent: () => import('./pages/ward-map/ward-map.component').then(m => m.WardMapComponent) },
  { path: 'admissions', loadComponent: () => import('./pages/admissions/admissions.component').then(m => m.AdmissionsComponent) },
  { path: 'admit', loadComponent: () => import('./pages/admit-discharge/admit-discharge.component').then(m => m.AdmitDischargeComponent) }
];
