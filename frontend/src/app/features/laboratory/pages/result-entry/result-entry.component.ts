import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { LabService } from '../../../../core/services/lab.service';
import { LabResult } from '../../../../core/models/lab.model';

@Component({
  selector: 'app-result-entry',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './result-entry.component.html',
  styleUrl: './result-entry.component.scss'
})
export class ResultEntryComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private service = inject(LabService);
  private fb = inject(FormBuilder);

  orderId = '';
  results: LabResult[] = [];
  loading = false;
  error = '';

  form = this.fb.group({
    order_item_id: ['', Validators.required],
    test_id: ['', Validators.required],
    patient_id: ['', Validators.required],
    result_value: ['', Validators.required],
    result_numeric: [''],
    unit_of_measure: [''],
    reference_range: [''],
    interpretation: ['NORMAL'],
    result_notes: [''],
    is_critical: [false]
  });

  ngOnInit(): void {
    this.orderId = this.route.snapshot.paramMap.get('id') || '';
    if (this.orderId) this.loadResults();
  }

  loadResults(): void {
    this.service.listResults(this.orderId).subscribe(r => this.results = r);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.service.addResult(this.orderId, this.form.value as any).subscribe({
      next: () => {
        this.loadResults();
        this.form.reset({ interpretation: 'NORMAL', is_critical: false });
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.detail || 'Failed to save result';
        this.loading = false;
      }
    });
  }
}