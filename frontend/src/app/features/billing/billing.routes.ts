import { Routes } from '@angular/router';

export const BILLING_ROUTES: Routes = [
  { path: '', redirectTo: 'invoices', pathMatch: 'full' },
  { path: 'invoices', loadComponent: () => import('./pages/invoice-list/invoice-list.component').then(m => m.InvoiceListComponent) },
  { path: 'invoices/:id', loadComponent: () => import('./pages/invoice-detail/invoice-detail.component').then(m => m.InvoiceDetailComponent) },
  { path: 'payments', loadComponent: () => import('./pages/payment/payment.component').then(m => m.PaymentComponent) }
];
