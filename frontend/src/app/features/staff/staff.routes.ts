import { Routes } from '@angular/router';

export const STAFF_ROUTES: Routes = [
  { path: '', loadComponent: () => import('./pages/list/list.component').then(m => m.ListComponent) },
  { path: ':id', loadComponent: () => import('./pages/detail/detail.component').then(m => m.DetailComponent) },
  { path: ':id/roster', loadComponent: () => import('./pages/roster/roster.component').then(m => m.RosterComponent) }
];
