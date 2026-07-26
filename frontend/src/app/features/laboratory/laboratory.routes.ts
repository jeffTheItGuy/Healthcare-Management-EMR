import { Routes } from '@angular/router';

export const LABORATORY_ROUTES: Routes = [
  { path: '', redirectTo: 'orders', pathMatch: 'full' },
  { path: 'catalog', loadComponent: () => import('./pages/catalog/catalog.component').then(m => m.CatalogComponent) },
  { path: 'orders', loadComponent: () => import('./pages/orders/orders.component').then(m => m.OrdersComponent) },
  { path: 'orders/new', loadComponent: () => import('./pages/order-create/order-create.component').then(m => m.OrderCreateComponent) },
  { path: 'orders/:id/results', loadComponent: () => import('./pages/result-entry/result-entry.component').then(m => m.ResultEntryComponent) }
];
