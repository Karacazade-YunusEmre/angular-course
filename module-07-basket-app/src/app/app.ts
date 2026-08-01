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
    return this.productService
      .products()
      .filter((curr) => !this.cartService.products().includes(curr));
  });
  protected readonly cardTotalPrice = computed(() => {
    let total = 0;
    this.cartService.products().forEach((product) => {
      total += product.price;
    });

    return total;
  });

  addToCard(id: string): void {
    const curr = this.productService.products().find((product) => product.id === id);
    if (!curr) return;

    this.cartService.addProduct(curr);
  }

  removeFromCard(product: Product): void {
    this.cartService.removeProduct(product);
  }

  clearToCard(): void {
    this.cartService.clearProducts();
  }
}
