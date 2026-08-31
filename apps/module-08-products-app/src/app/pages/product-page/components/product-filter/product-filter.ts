import { Component, DestroyRef, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Subject, debounceTime } from 'rxjs';
import { ProductService } from '@app/services/product-service';

@Component({
  imports: [],
  selector: 'app-product-filter',
  styleUrl: './product-filter.scss',
  templateUrl: './product-filter.html',
})
export class ProductFilter {
  private readonly productService = inject(ProductService);
  private readonly destroyRef = inject(DestroyRef);

  // Servisin signal'larını doğrudan okuyoruz: "Temizle" basıldığında
  // input'lar da boşalsın diye tek kaynak servis olmalı.
  protected readonly name = this.productService.name;
  protected readonly minPrice = this.productService.minPrice;
  protected readonly maxPrice = this.productService.maxPrice;
  protected readonly minStock = this.productService.minStock;
  protected readonly maxStock = this.productService.maxStock;
  protected readonly sort = this.productService.sort;

  // Her tuş vuruşunda istek atmamak için arama kutusu geciktiriliyor.
  private readonly nameInput = new Subject<string>();

  constructor() {
    this.nameInput
      .pipe(debounceTime(400), takeUntilDestroyed(this.destroyRef))
      .subscribe((value) => this.productService.setName(value));
  }

  protected onName(value: string): void {
    this.nameInput.next(value);
  }

  protected onMinPrice(value: string): void {
    this.productService.setMinPrice(this.toNumber(value));
  }

  protected onMaxPrice(value: string): void {
    this.productService.setMaxPrice(this.toNumber(value));
  }

  protected onMinStock(value: string): void {
    this.productService.setMinStock(this.toNumber(value));
  }

  protected onMaxStock(value: string): void {
    this.productService.setMaxStock(this.toNumber(value));
  }

  protected onSort(value: string): void {
    this.productService.setSelectedSort(value);
  }

  protected reset(): void {
    this.productService.resetFilters();
  }

  // Boş kutu NaN üretir; servis NaN'i "filtre yok" olarak ele alır.
  private toNumber(value: string): number {
    return value === '' ? Number.NaN : Number(value);
  }
}
