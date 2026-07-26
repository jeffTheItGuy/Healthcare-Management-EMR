import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { PatientService } from '../../../../core/services/patient.service';
import { Patient } from '../../../../core/models/patient.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-patient-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, DateFormatPipe],
  templateUrl: './detail.component.html',
  styleUrl: './detail.component.scss'
})
export class DetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private patientService = inject(PatientService);

  patient: Patient | null = null;
  loading = true;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) this.loadPatient(id);
  }

  loadPatient(id: string): void {
    this.patientService.get(id).subscribe({
      next: (p) => { this.patient = p; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }

  deletePatient(): void {
    if (!this.patient || !confirm('Delete this patient?')) return;
    this.patientService.delete(this.patient.patient_id).subscribe(() => {
      this.router.navigate(['/patients']);
    });
  }
}
