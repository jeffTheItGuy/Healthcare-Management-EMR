import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdmissionsService } from '../../../../core/services/admissions.service';
import { Ward, Bed } from '../../../../core/models/admissions.model';

@Component({
  selector: 'app-ward-map',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ward-map.component.html',
  styleUrl: './ward-map.component.scss'
})
export class WardMapComponent implements OnInit {
  private service = inject(AdmissionsService);
  wards: Ward[] = [];
  selectedWard: Ward | null = null;
  beds: Bed[] = [];

  ngOnInit(): void {
    this.service.listWards().subscribe(w => this.wards = w);
  }

  selectWard(ward: Ward): void {
    this.selectedWard = ward;
    this.service.listBeds(ward.ward_id).subscribe(b => this.beds = b);
  }
}
