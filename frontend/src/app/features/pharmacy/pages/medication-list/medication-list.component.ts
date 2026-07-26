import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { PharmacyService } from '../../../../core/services/pharmacy.service';
import { Medication } from '../../../../core/models/pharmacy.model';

@Component({
  selector: 'app-medication-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './medication-list.component.html',
  styleUrl: './medication-list.component.scss'
})
export class MedicationListComponent implements OnInit {
  private service = inject(PharmacyService);
  private fb = inject(FormBuilder);

  medications: Medication[] = [];
  showForm = false;

  form = this.fb.group({
    generic_name: ['', Validators.required],
    brand_name: [''],
    dosage_form: ['TABLET', Validators.required],
    strength: [''],
    category: [''],
    is_controlled: [false]
  });

  ngOnInit(): void { this.load(); }

  load(): void {
    this.service.listMedications().subscribe(m => this.medications = m);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.service.createMedication(this.form.value as any).subscribe(() => {
      this.load();
      this.showForm = false;
      this.form.reset({ dosage_form: 'TABLET', is_controlled: false });
    });
  }
}
