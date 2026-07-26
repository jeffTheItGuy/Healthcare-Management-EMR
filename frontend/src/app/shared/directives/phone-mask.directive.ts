import { Directive, ElementRef, HostListener, inject } from '@angular/core';

@Directive({
  selector: '[appPhoneMask]',
  standalone: true
})
export class PhoneMaskDirective {
  private el = inject(ElementRef<HTMLInputElement>);

  @HostListener('input', ['$event'])
  onInput(): void {
    let value = this.el.nativeElement.value.replace(/\D/g, '');
    if (value.length > 10) value = value.slice(0, 10);
    this.el.nativeElement.value = value;
  }
}
