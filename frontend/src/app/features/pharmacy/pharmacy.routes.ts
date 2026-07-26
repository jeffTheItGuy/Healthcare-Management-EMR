import { Routes } from '@angular/router';

export const PHARMACY_ROUTES: Routes = [
  { path: '', redirectTo: 'medications', pathMatch: 'full' },
  { path: 'medications', loadComponent: () => import('./pages/medication-list/medication-list.component').then(m => m.MedicationListComponent) },
  { path: 'inventory', loadComponent: () => import('./pages/inventory/inventory.component').then(m => m.InventoryComponent) },
  { path: 'dispense', loadComponent: () => import('./pages/dispense/dispense.component').then(m => m.DispenseComponent) }
];
