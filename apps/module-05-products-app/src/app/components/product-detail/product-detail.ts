import { Component, computed, input } from '@angular/core';
import { httpResource } from '@angular/common/http';
import { Product } from '../../models/product';
import { RouterLink } from '@angular/router';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-product-detail',
  imports: [RouterLink, DecimalPipe],
  templateUrl: './product-detail.html',
  styleUrl: './product-detail.scss',
})
export class ProductDetail {
  protected readonly id = input.required<string>();

  protected readonly product = httpResource<Product>(
    () => `https://dummyjson.com/products/${this.id()}`,
  );

  protected readonly oldPrice = computed(() => {
    const p = this.product.value();
    if (!p) return 0;

    return p.price / (1 - p.discountPercentage / 100);
  });
}
