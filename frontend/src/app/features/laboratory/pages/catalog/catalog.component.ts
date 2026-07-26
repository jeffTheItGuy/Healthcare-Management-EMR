import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { LabService } from '../../../../core/services/lab.service';
import { LabTestCatalog } from '../../../../core/models/lab.model';

@Component({
  selector: 'app-catalog',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './catalog.component.html',
  styleUrl: './catalog.component.scss'
})
export class CatalogComponent implements OnInit {
  private service = inject(LabService);
  private fb = inject(FormBuilder);

  tests: LabTestCatalog[] = [];
  showForm = false;
  loading = false;

  form = this.fb.group({
    test_code: ['', Validators.required],
    test_name: ['', Validators.required],
    category: [''],
    sample_type: [''],
    base_price: [''],
    currency_code: ['USD']
  });

  ngOnInit(): void { this.load(); }

  load(): void {
    this.service.listCatalog().subscribe(t => this.tests = t);
  }

  onSubmit(): void {
    if (this.form.invalid) return;
    this.service.createTestCatalog(this.form.value as any).subscribe(() => {
      this.load();
      this.showForm = false;
      this.form.reset({ currency_code: 'USD' });
    });
  }
}
