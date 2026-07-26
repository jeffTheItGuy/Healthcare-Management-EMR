import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { BillingService } from '../../../../core/services/billing.service';
import { BillingInvoice } from '../../../../core/models/billing.model';
import { CurrencyPipe } from '../../../../shared/pipes/currency.pipe';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';
import { StatusBadgePipe } from '../../../../shared/pipes/status-badge.pipe';

@Component({
  selector: 'app-invoice-list',
  standalone: true,
  imports: [CommonModule, RouterLink, CurrencyPipe, DateFormatPipe, StatusBadgePipe],
  templateUrl: './invoice-list.component.html',
  styleUrl: './invoice-list.component.scss'
})
export class InvoiceListComponent implements OnInit {
  private service = inject(BillingService);
  invoices: BillingInvoice[] = [];
  loading = false;

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    this.service.listInvoices().subscribe({
      next: (data) => { this.invoices = data; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
