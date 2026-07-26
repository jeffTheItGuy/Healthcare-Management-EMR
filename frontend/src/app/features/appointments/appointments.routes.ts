import { Routes } from '@angular/router';

export const APPOINTMENT_ROUTES: Routes = [
  { path: '', loadComponent: () => import('./pages/list/list.component').then(m => m.ListComponent) },
  { path: 'new', loadComponent: () => import('./pages/booking/booking.component').then(m => m.BookingComponent) }
];
