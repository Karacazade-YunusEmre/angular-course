import { Service, signal } from '@angular/core';
import { Product } from '../../models/product';

@Service()
export class CartService {
  private readonly _products = signal<Product[]>([]);
  readonly products = this._products.asReadonly();

  addProduct(product: Product) {
    this._products.update((curr) => [...curr, product]);
  }

  removeProduct(product: Product) {
    this._products.update((curr) => curr.filter((i) => i !== product));
  }

  clearProducts(): void {
    this._products.set([]);
  }
}
