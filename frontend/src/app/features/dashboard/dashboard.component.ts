import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';
import { PatientService } from '../../core/services/patient.service';
import { AppointmentsService } from '../../core/services/appointments.service';
import { AdmissionsService } from '../../core/services/admissions.service';
import { CurrencyPipe } from '../../shared/pipes/currency.pipe';
import { StatusBadgePipe } from '../../shared/pipes/status-badge.pipe';
import { DateFormatPipe } from '../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, CurrencyPipe, StatusBadgePipe, DateFormatPipe],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  private patientService = inject(PatientService);
  private appointmentService = inject(AppointmentsService);
  private admissionService = inject(AdmissionsService);
  auth = inject(AuthService);

  stats = {
    totalPatients: 0,
    todayAppointments: 0,
    admittedPatients: 0,
    pendingLabOrders: 0
  };

  recentAppointments: any[] = [];
  recentAdmissions: any[] = [];

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.patientService.list().subscribe(p => this.stats.totalPatients = p.length);
    this.appointmentService.list(undefined, new Date().toISOString().split('T')[0]).subscribe(a => {
      this.stats.todayAppointments = a.length;
      this.recentAppointments = a.slice(0, 5);
    });
    this.admissionService.listAdmissions(undefined, 'ADMITTED').subscribe(ad => {
      this.stats.admittedPatients = ad.length;
      this.recentAdmissions = ad.slice(0, 5);
    });
  }
}
