import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { PatientService } from '../../../../core/services/patient.service';
import { PatientCreate, PatientUpdate } from '../../../../core/models/patient.model';

@Component({
  selector: 'app-patient-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './form.component.html',
  styleUrl: './form.component.scss'
})
export class FormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private patientService = inject(PatientService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  patientId: string | null = null;
  loading = false;
  error = '';

  form = this.fb.group({
    patient_number: ['', Validators.required],
    national_id: [''],
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    date_of_birth: ['', Validators.required],
    gender: ['MALE', Validators.required],
    blood_group: [''],
    phone_primary: [''],
    phone_secondary: [''],
    email: [''],
    address: [''],
    city: [''],
    suburb: [''],
    emergency_contact_name: [''],
    emergency_contact_phone: [''],
    medical_aid_number: [''],
    medical_aid_plan: [''],
    allergies: [''],
    chronic_conditions: [''],
    is_active: [true]
  });

  ngOnInit(): void {
    this.patientId = this.route.snapshot.paramMap.get('id');
    if (this.patientId) {
      this.patientService.get(this.patientId).subscribe(p => {
        this.form.patchValue(p as any);
      });
    }
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    this.error = '';

    const value = this.form.value;
    if (this.patientId) {
      this.patientService.update(this.patientId, value as PatientUpdate).subscribe({
        next: () => this.router.navigate(['/patients', this.patientId]),
        error: (err) => { this.error = err.error?.detail || 'Update failed'; this.loading = false; }
      });
    } else {
      this.patientService.create(value as PatientCreate).subscribe({
        next: (p) => this.router.navigate(['/patients', p.patient_id]),
        error: (err) => { this.error = err.error?.detail || 'Creation failed'; this.loading = false; }
      });
    }
  }
}
