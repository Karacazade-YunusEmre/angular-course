import { Component, computed, signal } from '@angular/core';
import { httpResource } from '@angular/common/http';
import { ProductResponse } from '../../models/product';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-product-list',
  imports: [RouterLink],
  templateUrl: './product-list.html',
  styleUrl: './product-list.scss',
})
export class ProductList {
  protected readonly productResponse = httpResource<ProductResponse>(
    () => 'https://dummyjson.com/products',
  );
  protected readonly filterText = signal('');
  protected readonly filtered = computed(() => {
    const products = this.productResponse.value()?.products ?? [];
    const query = this.filterText().toLowerCase();
    return products.filter((product) => product.title.toLowerCase().includes(query));
  });

  protected filterTextOnChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.filterText.set(input.value);
  }
}
