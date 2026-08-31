import { Service, signal } from '@angular/core';
import { Product } from '../../models/product';

@Service()
export class ProductService {
  private readonly _products = signal<Product[]>([
    { id: '1', name: 'Kablosuz Kulaklık', price: 899.9 },
    { id: '2', name: 'Mekanik Klavye', price: 1249.5 },
    { id: '3', name: 'Bluetooth Hoparlör', price: 649.0 },
    { id: '4', name: 'Akıllı Bileklik', price: 399.99 },
  ]);
  readonly products = this._products.asReadonly();
}
