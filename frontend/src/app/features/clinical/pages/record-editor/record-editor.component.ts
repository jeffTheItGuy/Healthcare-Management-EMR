import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MedicalService } from '../../../../core/services/medical.service';

@Component({
  selector: 'app-record-editor',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './record-editor.component.html',
  styleUrl: './record-editor.component.scss'
})
export class RecordEditorComponent implements OnInit {
  private fb = inject(FormBuilder);
  private service = inject(MedicalService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);

  recordId: string | null = null;
  loading = false;
  error = '';

  form = this.fb.group({
    patient_id: ['', Validators.required],
    encounter_type: ['OPD', Validators.required],
    chief_complaint: [''],
    history_of_present_illness: [''],
    physical_examination: [''],
    assessment_and_plan: [''],
    vital_signs: this.fb.group({
      temperature: [''],
      blood_pressure: [''],
      pulse: [''],
      respiratory_rate: [''],
      spo2: ['']
    })
  });

  ngOnInit(): void {
    this.recordId = this.route.snapshot.paramMap.get('id');
    // Only fetch if editing an existing record, not when creating new
    if (this.recordId && this.recordId !== 'new') {
      this.service.getRecord(this.recordId).subscribe(r => {
        this.form.patchValue({
          ...r,
          vital_signs: r.vital_signs || {}
        } as any);
      });
    }
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.loading = true;
    const value = this.form.value;
    if (this.recordId && this.recordId !== 'new') {
      // update not implemented in service yet
      this.router.navigate(['/clinical/records', this.recordId]);
    } else {
      this.service.createRecord(value as any).subscribe({
        next: (r) => this.router.navigate(['/clinical/records', r.record_id]),
        error: (err) => { this.error = err.error?.detail || 'Failed'; this.loading = false; }
      });
    }
  }
}