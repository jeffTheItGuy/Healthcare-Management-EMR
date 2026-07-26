import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LabService } from '../../../../core/services/lab.service';

@Component({
  selector: 'app-order-create',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './order-create.component.html',
  styleUrl: './order-create.component.scss'
})
export class OrderCreateComponent {
  private fb = inject(FormBuilder);
  private service = inject(LabService);
  private router = inject(Router);

  form = this.fb.group({
    order_number: ['', Validators.required],
    patient_id: ['', Validators.required],
    priority: ['ROUTINE'],
    clinical_notes: ['']
  });

  loading = false;
  error = '';

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.service.createOrder(this.form.value as any).subscribe({
      next: () => this.router.navigate(['/lab/orders']),
      error: (err) => { this.error = err.error?.detail || 'Failed'; this.loading = false; }
    });
  }
}
