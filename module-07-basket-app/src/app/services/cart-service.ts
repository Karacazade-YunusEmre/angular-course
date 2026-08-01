import { computed, Service, signal } from '@angular/core';
import { Product } from '../../models/product';

@Service()
export class CartService {
  private readonly _products = signal<Product[]>([]);
  readonly products = this._products.asReadonly();
  readonly total = computed(() => {
    return this._products().reduce((sum, prod) => sum + prod.price, 0);
  });
  readonly count = computed(() => this._products().length);

  addProduct(product: Product) {
    this._products.update((curr) => [...curr, product]);
  }

  removeProduct(id: string) {
    this._products.update((curr) => curr.filter((i) => i.id !== id));
  }

  clearProducts(): void {
    this._products.set([]);
  }
}
