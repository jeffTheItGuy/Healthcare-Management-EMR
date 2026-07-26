import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AdmissionsService } from '../../../../core/services/admissions.service';

@Component({
  selector: 'app-admit-discharge',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './admit-discharge.component.html',
  styleUrl: './admit-discharge.component.scss'
})
export class AdmitDischargeComponent {
  private fb = inject(FormBuilder);
  private service = inject(AdmissionsService);
  private router = inject(Router);

  mode: 'admit' | 'discharge' = 'admit';
  loading = false;
  error = '';

  admitForm = this.fb.group({
    patient_id: ['', Validators.required],
    bed_id: [''],
    admission_number: ['', Validators.required],
    admission_type: ['EMERGENCY', Validators.required]
  });

  dischargeForm = this.fb.group({
    admission_id: ['', Validators.required],
    discharge_type: ['HOME'],
    discharge_summary: ['']
  });

  onAdmit(): void {
    if (this.admitForm.invalid) return;
    this.loading = true;
    this.service.admit(this.admitForm.value as any).subscribe({
      next: () => this.router.navigate(['/clinical/admissions']),
      error: (err) => { this.error = err.error?.detail || 'Admit failed'; this.loading = false; }
    });
  }

  onDischarge(): void {
    if (this.dischargeForm.invalid) return;
    this.loading = true;
    const { admission_id, ...update } = this.dischargeForm.value;
    this.service.discharge(admission_id!, update as any).subscribe({
      next: () => this.router.navigate(['/clinical/admissions']),
      error: (err) => { this.error = err.error?.detail || 'Discharge failed'; this.loading = false; }
    });
  }
}
