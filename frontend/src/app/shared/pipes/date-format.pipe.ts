import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormat',
  standalone: true
})
export class DateFormatPipe implements PipeTransform {
  transform(value: string | Date | null, format: 'short' | 'medium' | 'long' = 'short'): string {
    if (!value) return '-';
    const date = new Date(value);
    if (isNaN(date.getTime())) return String(value);
    if (format === 'short') return date.toLocaleDateString('en-GB');
    if (format === 'medium') return date.toLocaleString('en-GB');
    return date.toISOString();
  }
}
