import { Component, computed, inject } from '@angular/core';
import { ProductService } from './services/product-service';
import { CurrencyPipe } from '@angular/common';
import { Product } from '../models/product';
import { CartService } from './services/cart-service';

@Component({
  selector: 'app-root',
  imports: [CurrencyPipe],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly productService = inject(ProductService);
  protected readonly cartService = inject(CartService);

  protected readonly productList = computed(() => {
    const cartIds = new Set<string>(this.cartService.products().map((i) => i.id));
    return this.productService.products().filter((curr) => !cartIds.has(curr.id));
  });

  addToCart(id: string): void {
    const curr = this.productService.products().find((product) => product.id === id);
    if (!curr) return;

    this.cartService.addProduct(curr);
  }

  removeFromCart(product: Product): void {
    this.cartService.removeProduct(product.id);
  }

  clearCart(): void {
    this.cartService.clearProducts();
  }
}
