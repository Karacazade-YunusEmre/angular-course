import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'truncate' })
export class TruncatePipe implements PipeTransform {
  transform(value: string, count: number = 40): string {
    if (!value) return '';

    return value.length > count ? value.slice(0, count) + '...' : value;
  }
}
