import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { BillingService } from '../../../../core/services/billing.service';

@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './payment.component.html',
  styleUrl: './payment.component.scss'
})
export class PaymentComponent {
  private fb = inject(FormBuilder);
  private service = inject(BillingService);
  private router = inject(Router);

  form = this.fb.group({
    invoice_id: ['', Validators.required],
    patient_id: ['', Validators.required],
    payment_method: ['CASH', Validators.required],
    amount: ['', Validators.required],
    currency_code: ['USD'],
    reference_number: ['']
  });

  loading = false;
  error = '';

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    const { invoice_id, ...payment } = this.form.value;
    this.service.addPayment(invoice_id!, payment as any).subscribe({
      next: () => this.router.navigate(['/billing/invoices']),
      error: (err) => { this.error = err.error?.detail || 'Payment failed'; this.loading = false; }
    });
  }
}
