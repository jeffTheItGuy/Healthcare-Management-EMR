import { Pipe, PipeTransform } from '@angular/core';
import { CurrencyService } from '../../core/services/currency.service';

@Pipe({
  name: 'currency',
  standalone: true
})
export class CurrencyPipe implements PipeTransform {
  constructor(private service: CurrencyService) {}

  transform(value: string | number | null, currencyCode: string = 'USD'): string {
    return this.service.format(value, currencyCode as any);
  }
}
