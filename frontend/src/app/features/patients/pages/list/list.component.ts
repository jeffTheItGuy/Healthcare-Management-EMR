import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { PatientService } from '../../../../core/services/patient.service';
import { Patient } from '../../../../core/models/patient.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-patient-list',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule, DateFormatPipe],
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss'
})
export class ListComponent implements OnInit {
  private patientService = inject(PatientService);
  private fb = inject(FormBuilder);

  patients: Patient[] = [];
  loading = false;
  searchControl = this.fb.control('');

  ngOnInit(): void {
    this.loadPatients();
    this.searchControl.valueChanges.subscribe(q => this.loadPatients(q || undefined));
  }

  loadPatients(q?: string): void {
    this.loading = true;
    this.patientService.list(q).subscribe({
      next: (data) => { this.patients = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
