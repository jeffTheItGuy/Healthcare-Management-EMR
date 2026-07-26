import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { SearchService } from '../../../../core/services/search.service';
import { DocumentSearchResult } from '../../../../core/models/search.model';

@Component({
  selector: 'app-documents',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './documents.component.html',
  styleUrl: './documents.component.scss'
})
export class DocumentsComponent {
  private fb = inject(FormBuilder);
  private service = inject(SearchService);

  form = this.fb.group({
    query: ['', Validators.required],
    top_k: [5]
  });

  results: DocumentSearchResult[] = [];
  loading = false;

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.service.searchDocuments(this.form.value as any).subscribe({
      next: (data) => { this.results = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
