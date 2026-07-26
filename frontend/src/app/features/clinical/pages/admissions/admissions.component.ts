import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AdmissionsService } from '../../../../core/services/admissions.service';
import { Admission } from '../../../../core/models/admissions.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';
import { StatusBadgePipe } from '../../../../shared/pipes/status-badge.pipe';

@Component({
  selector: 'app-admissions',
  standalone: true,
  imports: [CommonModule, RouterLink, DateFormatPipe, StatusBadgePipe],
  templateUrl: './admissions.component.html',
  styleUrl: './admissions.component.scss'
})
export class AdmissionsComponent implements OnInit {
  private service = inject(AdmissionsService);
  admissions: Admission[] = [];
  loading = false;

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    this.service.listAdmissions().subscribe({
      next: (data) => { this.admissions = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
