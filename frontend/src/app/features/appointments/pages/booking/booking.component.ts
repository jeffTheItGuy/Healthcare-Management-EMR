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
    staff_id: [''],
    appointment_date: ['', Validators.required],
    appointment_type: ['OPD_CONSULTATION', Validators.required],
    notes: ['']
  });

  loading = false;
  error = '';

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.service.create(this.form.value as any).subscribe({
      next: () => this.router.navigate(['/appointments']),
      error: (err) => { this.error = err.error?.detail || 'Booking failed'; this.loading = false; }
    });
  }
}
