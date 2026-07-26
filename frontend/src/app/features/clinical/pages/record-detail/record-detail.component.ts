import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { MedicalService } from '../../../../core/services/medical.service';
import { MedicalRecord } from '../../../../core/models/medical.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-record-detail',
  standalone: true,
  imports: [CommonModule, DateFormatPipe],
  templateUrl: './record-detail.component.html',
  styleUrl: './record-detail.component.scss'
})
export class RecordDetailComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private service = inject(MedicalService);
  record: MedicalRecord | null = null;
  loading = true;

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) this.service.getRecord(id).subscribe({
      next: (r) => { this.record = r; this.loading = false; },
      error: () => { this.loading = false; }
    });
  }
}
