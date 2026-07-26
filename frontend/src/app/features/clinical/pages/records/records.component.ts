import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MedicalService } from '../../../../core/services/medical.service';
import { MedicalRecord } from '../../../../core/models/medical.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-records',
  standalone: true,
  imports: [CommonModule, RouterLink, DateFormatPipe],
  templateUrl: './records.component.html',
  styleUrl: './records.component.scss'
})
export class RecordsComponent implements OnInit {
  private service = inject(MedicalService);
  records: MedicalRecord[] = [];
  loading = false;

  ngOnInit(): void { this.load(); }

  load(): void {
    this.loading = true;
    // In a real app you'd have a list endpoint; simulating with empty for now
    this.loading = false;
  }
}
