import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { StaffService } from '../../../../core/services/staff.service';
import { StaffRoster } from '../../../../core/models/staff.model';
import { DateFormatPipe } from '../../../../shared/pipes/date-format.pipe';

@Component({
  selector: 'app-roster',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, DateFormatPipe],
  templateUrl: './roster.component.html',
  styleUrl: './roster.component.scss'
})
export class RosterComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private service = inject(StaffService);
  private fb = inject(FormBuilder);

  staffId = '';
  roster: StaffRoster[] = [];
  showForm = false;

  form = this.fb.group({
    roster_date: ['', Validators.required],
    shift_type: ['MORNING', Validators.required],
    start_time: [''],
    end_time: [''],
    ward_id: [''],
    notes: ['']
  });

  ngOnInit(): void {
    this.staffId = this.route.snapshot.paramMap.get('id') || '';
    this.load();
  }

  load(): void {
    this.service.getRoster(this.staffId).subscribe(r => this.roster = r);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.service.addRoster(this.staffId, this.form.value as any).subscribe(() => {
      this.load();
      this.showForm = false;
      this.form.reset({ shift_type: 'MORNING' });
    });
  }
}
