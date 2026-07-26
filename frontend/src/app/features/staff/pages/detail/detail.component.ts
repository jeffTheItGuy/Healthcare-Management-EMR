import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { StaffService } from '../../../../core/services/staff.service';
import { Staff } from '../../../../core/models/staff.model';

@Component({
  selector: 'app-staff-detail',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './detail.component.html',
  styleUrl: './detail.component.scss'
})
export class DetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private service = inject(StaffService);
  staff: Staff | null = null;
  loading = true;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) this.service.getStaff(id).subscribe({
      next: (s) => { this.staff = s; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
