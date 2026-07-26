import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { AppointmentsService } from '../../../../core/services/appointments.service';
import { Appointment } from '../../../../core/models/appointments.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';
import { StatusBadgePipe } from '../../../../shared/pipes/status-badge.pipe';

@Component({
  selector: 'app-appointment-list',
  standalone: true,
  imports: [CommonModule, RouterLink, ReactiveFormsModule, DateFormatPipe, StatusBadgePipe],
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss'
})
export class ListComponent implements OnInit {
  private service = inject(AppointmentsService);
  private fb = inject(FormBuilder);

  appointments: Appointment[] = [];
  loading = false;
  filter = this.fb.group({ status: [''], date: [''] });

  ngOnInit(): void {
    this.load();
    this.filter.valueChanges.subscribe(() => this.load());
  }

  load(): void {
    this.loading = true;
    const { status, date } = this.filter.value;
    this.service.list(undefined, date || undefined, undefined, status || undefined).subscribe({
      next: (data) => { this.appointments = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }

  cancel(id: string): void {
    if (!confirm('Cancel this appointment?')) return;
    this.service.cancel(id).subscribe(() => this.load());
  }
}
