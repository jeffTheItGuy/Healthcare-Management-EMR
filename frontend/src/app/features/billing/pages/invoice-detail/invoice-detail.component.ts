import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { BillingService } from '../../../../core/services/billing.service';
import { BillingInvoice } from '../../../../core/models/billing.model';
import { CurrencyPipe } from '../../../../shared/pipes/currency.pipe';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-invoice-detail',
  standalone: true,
  imports: [CommonModule, CurrencyPipe, DateFormatPipe],
  templateUrl: './invoice-detail.component.html',
  styleUrl: './invoice-detail.component.scss'
})
export class InvoiceDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private service = inject(BillingService);
  invoice: BillingInvoice | null = null;
  loading = true;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) this.service.getInvoice(id).subscribe({
      next: (inv) => { this.invoice = inv; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
