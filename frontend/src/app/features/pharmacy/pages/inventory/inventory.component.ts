import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PharmacyService } from '../../../../core/services/pharmacy.service';
import { PharmacyInventory } from '../../../../core/models/pharmacy.model';

@Component({
  selector: 'app-inventory',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inventory.component.html',
  styleUrl: './inventory.component.scss'
})
export class InventoryComponent implements OnInit {
  private service = inject(PharmacyService);
  inventory: PharmacyInventory[] = [];

  ngOnInit(): void {
    this.service.listInventory().subscribe(i => this.inventory = i);
  }
}
