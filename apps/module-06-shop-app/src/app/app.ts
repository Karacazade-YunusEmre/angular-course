import { Component, signal } from '@angular/core';
import { Order } from './models/order';
import { CurrencyPipe, DatePipe, PercentPipe, TitleCasePipe } from '@angular/common';
import { StatusColor } from './directives/status-color';
import { OrderStatusPipe } from './pipes/order-status-pipe';
import { TruncatePipe } from './pipes/truncate-pipe';

@Component({
  selector: 'app-root',
  imports: [
    TitleCasePipe,
    DatePipe,
    CurrencyPipe,
    PercentPipe,
    StatusColor,
    OrderStatusPipe,
    TruncatePipe,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly orders = signal<Order[]>([
    {
      id: 1,
      customerName: 'ayşe yılmaz',
      orderDate: new Date('2026-07-14'),
      totalPrice: 1712,
      discount: 0.1,
      status: 'shipped',
      description: 'Kapıda ödeme, akşam teslim tercih edildi; zili çalmadan kapıya bırakın lütfen.',
    },
    {
      id: 2,
      customerName: 'mehmet demir',
      orderDate: new Date('2026-07-13'),
      totalPrice: 429.9,
      discount: 0,
      status: 'pending',
      description: 'Fatura adresi ile teslim adresi farklı, dikkat edilsin.',
    },
    {
      id: 3,
      customerName: 'zeynep kaya',
      orderDate: new Date('2026-07-11'),
      totalPrice: 3058.5,
      discount: 0.15,
      status: 'delivered',
      description: 'Hediye paketi istendi, not kartı eklendi.',
    },
    {
      id: 4,
      customerName: 'can öztürk',
      orderDate: new Date('2026-07-09'),
      totalPrice: 89,
      discount: 0,
      status: 'cancelled',
      description: 'Müşteri talebiyle iptal edildi.',
    },
  ]);
}
