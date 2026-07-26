import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  auth = inject(AuthService);

  navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: '📊' },
    { label: 'Patients', path: '/patients', icon: '🏥' },
    { label: 'Appointments', path: '/appointments', icon: '📅' },
    { label: 'Clinical', path: '/clinical', icon: '📋' },
    { label: 'Laboratory', path: '/lab', icon: '🧪', roles: ['DOCTOR','NURSE','LAB_TECH','ADMIN','MANAGER'] },
    { label: 'Pharmacy', path: '/pharmacy', icon: '💊', roles: ['PHARMACIST','DOCTOR','ADMIN','MANAGER'] },
    { label: 'Billing', path: '/billing', icon: '💵', roles: ['CASHIER','ADMIN','MANAGER'] },
    { label: 'Staff', path: '/staff', icon: '👤', roles: ['ADMIN','MANAGER'] },
    { label: 'Search', path: '/search', icon: '🔍' },
  ];

  visibleItems() {
    const role = this.auth.currentUserValue?.role;
    return this.navItems.filter(i => !i.roles || i.roles.includes(role!));
  }
}
