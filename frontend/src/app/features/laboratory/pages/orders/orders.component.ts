import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LabService } from '../../../../core/services/lab.service';
import { LabOrder } from '../../../../core/models/lab.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';
import { StatusBadgePipe } from '../../../../shared/pipes/status-badge.pipe';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, RouterLink, DateFormatPipe, StatusBadgePipe],
  templateUrl: './orders.component.html',
  styleUrl: './orders.component.scss'
})
export class OrdersComponent implements OnInit {
  private service = inject(LabService);
  orders: LabOrder[] = [];
  loading = false;

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    this.service.listOrders().subscribe({
      next: (data) => { this.orders = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
