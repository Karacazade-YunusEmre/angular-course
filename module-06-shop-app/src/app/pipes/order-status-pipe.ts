import { Pipe, PipeTransform } from '@angular/core';
import { OrderStatus } from '../models/order';

@Pipe({ name: 'orderStatus' })
export class OrderStatusPipe implements PipeTransform {
  transform(value: OrderStatus): string {
    const labels: Record<OrderStatus, string> = {
      pending: 'Bekliyor',
      shipped: 'Kargoda',
      delivered: 'Teslim Edildi',
      cancelled: 'İptal Edildi',
    };

    return labels[value];
  }
}
