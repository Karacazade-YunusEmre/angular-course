import { computed, Directive, input } from '@angular/core';
import { OrderStatus } from '../models/order';

@Directive({
  selector: '[appStatusColor]',
  host: {
    '[style.background-color]': 'color()',
  },
})
export class StatusColor {
  public readonly appStatusColor = input<OrderStatus>();
  protected readonly color = computed(() => {
    switch (this.appStatusColor()) {
      case 'pending':
        return '#f59e0b';
      case 'shipped':
        return '#3b82f6';
      case 'delivered':
        return '#22a06b';
      case 'cancelled':
        return '#ef4444';
    }

    return;
  });
}
