import { Directive, ElementRef, HostListener, inject } from '@angular/core';

@Directive({
  selector: '[appNationalIdMask]',
  standalone: true
})
export class NationalIdMaskDirective {
  private el = inject(ElementRef<HTMLInputElement>);

  @HostListener('input')
  onInput(): void {
    let v = this.el.nativeElement.value.toUpperCase().replace(/[^0-9A-Z-]/g, '');
    this.el.nativeElement.value = v;
  }
}
