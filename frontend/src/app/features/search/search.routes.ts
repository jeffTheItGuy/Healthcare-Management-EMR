import { Routes } from '@angular/router';

export const SEARCH_ROUTES: Routes = [
  { path: '', redirectTo: 'documents', pathMatch: 'full' },
  { path: 'documents', loadComponent: () => import('./pages/documents/documents.component').then(m => m.DocumentsComponent) },
  { path: 'patients', loadComponent: () => import('./pages/similarity/similarity.component').then(m => m.SimilarityComponent) }
];
