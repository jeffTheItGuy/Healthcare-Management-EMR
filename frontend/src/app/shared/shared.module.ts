import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// Standalone directives & pipes are imported directly in components.
// This module exists only for legacy compatibility if needed.

@NgModule({
  imports: [CommonModule],
  exports: [CommonModule]
})
export class SharedModule {}
