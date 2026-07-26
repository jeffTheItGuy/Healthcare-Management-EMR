import { Injectable } from '@angular/core';

export type CurrencyCode = 'USD' | 'ZiG' | 'ZWL';

@Injectable({ providedIn: 'root' })
export class CurrencyService {
  private readonly rates: Record<CurrencyCode, number> = {
    USD: 1.0,
    ZiG: 13.5,
    ZWL: 1000.0,
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
    switch (currency) {
      case 'USD':
        return `$${amt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      case 'ZiG':
        return `ZiG ${amt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      case 'ZWL':
        return `ZWL ${amt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      default:
        return `${currency} ${amt.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
  }

  validatePaymentMethod(method: string, currency: string): boolean {
    const m = method.toUpperCase();
    const c = currency.toUpperCase();
    if (['CASH', 'USD_CASH', 'ZiG_CASH'].includes(m)) return true;
    if (m === 'ECOCASH') return ['ZiG', 'ZWL'].includes(c);
    if (['ZIPIT', 'BANK_TRANSFER', 'CARD'].includes(m)) return true;
    if (m === 'MEDICAL_AID') return c === 'USD';
    return true;
  }
}
