import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { PharmacyService } from '../../../../core/services/pharmacy.service';

@Component({
  selector: 'app-dispense',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './dispense.component.html',
  styleUrl: './dispense.component.scss'
})
export class DispenseComponent {
  private fb = inject(FormBuilder);
  private service = inject(PharmacyService);
  private router = inject(Router);

  form = this.fb.group({
    prescription_item_id: ['', Validators.required],
    batch_id: [''],
    patient_id: ['', Validators.required],
    quantity_dispensed: ['', Validators.required],
    unit_price: [''],
    currency_code: ['USD']
  });

  loading = false;
  error = '';

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.service.dispense(this.form.value as any).subscribe({
      next: () => this.router.navigate(['/pharmacy/inventory']),
      error: (err) => { this.error = err.error?.detail || 'Dispense failed'; this.loading = false; }
    });
  }
}
