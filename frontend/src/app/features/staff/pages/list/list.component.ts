import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { StaffService } from '../../../../core/services/staff.service';
import { Staff } from '../../../../core/models/staff.model';

@Component({
  selector: 'app-staff-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss'
})
export class ListComponent implements OnInit {
  private service = inject(StaffService);
  staff: Staff[] = [];
  loading = false;

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    this.service.listStaff().subscribe({
      next: (data) => { this.staff = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
