export type OrderStatus = 'pending' | 'shipped' | 'delivered' | 'cancelled';

export interface Order {
  readonly id: number;
  customerName: string;
  orderDate: Date;
  totalPrice: number;
  discount: number; // 0–1 arası (percent pipe için), ör. 0.1 = %10
  status: OrderStatus;
  description: string;
}
