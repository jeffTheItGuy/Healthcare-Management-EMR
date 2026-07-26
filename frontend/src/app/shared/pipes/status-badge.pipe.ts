import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'statusBadge',
  standalone: true
})
export class StatusBadgePipe implements PipeTransform {
  transform(status: string | null): string {
    const map: Record<string, string> = {
      SCHEDULED: 'badge-info',
      CHECKED_IN: 'badge-primary',
      IN_PROGRESS: 'badge-warning',
      COMPLETED: 'badge-success',
      CANCELLED: 'badge-danger',
      NO_SHOW: 'badge-muted',
      ADMITTED: 'badge-warning',
      DISCHARGED: 'badge-success',
      TRANSFERRED: 'badge-info',
      AVAILABLE: 'badge-success',
      OCCUPIED: 'badge-danger',
      MAINTENANCE: 'badge-warning',
      RESERVED: 'badge-info',
      UNPAID: 'badge-danger',
      PARTIAL: 'badge-warning',
      PAID: 'badge-success',
      OVERPAID: 'badge-info',
      WRITTEN_OFF: 'badge-muted',
      PENDING: 'badge-warning',
      DISPENSED: 'badge-success',
      NORMAL: 'badge-success',
      ABNORMAL: 'badge-warning',
      CRITICAL: 'badge-danger',
      BORDERLINE: 'badge-info',
      ORDERED: 'badge-info',
      ACTIVE: 'badge-success',
      INACTIVE: 'badge-muted',
    };
    return map[(status || '').toUpperCase()] || 'badge-muted';
  }
}
