import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { SearchService } from '../../../../core/services/search.service';
import { PatientSimilarityResult } from '../../../../core/models/search.model';

@Component({
  selector: 'app-similarity',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './similarity.component.html',
  styleUrl: './similarity.component.scss'
})
export class SimilarityComponent {
  private fb = inject(FormBuilder);
  private service = inject(SearchService);

  form = this.fb.group({
    patient_id: ['', Validators.required],
    top_k: [5]
  });

  results: PatientSimilarityResult[] = [];
  loading = false;

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.service.findSimilarPatients(this.form.value as any).subscribe({
      next: (data) => { this.results = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
