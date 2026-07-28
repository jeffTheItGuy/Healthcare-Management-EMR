import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AppointmentsService } from '../../../../core/services/appointments.service';

@Component({
  selector: 'app-booking',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './booking.component.html',
  styleUrl: './booking.component.scss'
})
export class BookingComponent {
  private fb = inject(FormBuilder);
  private service = inject(AppointmentsService);
  private router = inject(Router);

  form = this.fb.group({
    patient_id: ['', Validators.required],
    doctor_id: [''],
    department_id: [''],
    appointment_number: ['', Validators.required],
    scheduled_date: ['', Validators.required],
    scheduled_time: [''],
    estimated_duration_minutes: [null as number | null],
    appointment_type: ['OPD_CONSULTATION', Validators.required],
    chief_complaint: [''],
    notes: ['']
  });

  loading = false;
  error = '';

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;

    const value = this.form.value as any;

    // Auto-generate appointment number if left empty
    if (!value.appointment_number) {
      const now = new Date();
      const pad = (n: number) => n.toString().padStart(2, '0');
      const random = Math.floor(1000 + Math.random() * 9000);
      value.appointment_number = `APT-${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}-${random}`;
    }

    this.service.create(value).subscribe({
      next: () => this.router.navigate(['/appointments']),
      error: (err) => { this.error = err.error?.detail || 'Booking failed'; this.loading = false; }
    });
  }
}