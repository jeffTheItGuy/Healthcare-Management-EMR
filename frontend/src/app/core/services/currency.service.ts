import { Injectable } from '@angular/core';

export type CurrencyCode = 'USD' | 'EUR' | 'GBP' | 'ZAR';

@Injectable({ providedIn: 'root' })
export class CurrencyService {
  private readonly rates: Record<CurrencyCode, number> = {
    USD: 1.0,
    EUR: 0.92,
    GBP: 0.79,
    ZAR: 18.5,
  };

  toDecimal(value: string | number | null): number {
    if (value === null || value === undefined) return 0;
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return isNaN(num) ? 0 : num;
  }

  getExchangeRate(currency: CurrencyCode): number {
    return this.rates[currency] ?? 1.0;
  }

  convertToBase(amount: string | number, currency: CurrencyCode, exchangeRate?: number): number {
    const amt = this.toDecimal(amount);
    if (currency === 'USD') return parseFloat(amt.toFixed(2));
    const rate = exchangeRate ?? this.getExchangeRate(currency);
    return parseFloat((amt / rate).toFixed(2));
  }

  convertFromBase(amount: string | number, target: CurrencyCode, exchangeRate?: number): number {
    const amt = this.toDecimal(amount);
    if (target === 'USD') return parseFloat(amt.toFixed(2));
    const rate = exchangeRate ?? this.getExchangeRate(target);
    return parseFloat((amt * rate).toFixed(2));
  }

  format(amount: string | number, currency: CurrencyCode = 'USD'): string {
    const amt = this.toDecimal(amount);
    const formatted = amt.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
    switch (currency) {
      case 'USD': return `$${formatted}`;
      case 'EUR': return `€${formatted}`;
      case 'GBP': return `£${formatted}`;
      default:    return `${currency} ${formatted}`;
    }
  }

  validatePaymentMethod(method: string, currency: string): boolean {
    const m = method.toUpperCase();
    const c = currency.toUpperCase();
    const allowed = [
      'CASH', 'CARD', 'BANK_TRANSFER',
      'MOBILE_MONEY', 'INSURANCE', 'MEDICAL_AID'
    ];
    return allowed.includes(m) && !!c;
  }
}
