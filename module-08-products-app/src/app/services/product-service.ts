import { computed, inject, Service, signal } from '@angular/core';
import { HttpClient, httpResource } from '@angular/common/http';
import { PagedResult } from '@app/models/paged-result';
import { Product } from '@app/models/product';
import { Observable, tap } from 'rxjs';

@Service()
export class ProductService {
  private readonly httpClient = inject(HttpClient);

  readonly currentPage = signal(1);
  readonly pageSize = signal(5);

  readonly name = signal<string | undefined>(undefined);
  readonly minPrice = signal<number | undefined>(undefined);
  readonly maxPrice = signal<number | undefined>(undefined);
  readonly minStock = signal<number | undefined>(undefined);
  readonly maxStock = signal<number | undefined>(undefined);
  readonly sort = signal<string | undefined>(undefined);

  private buildParams(): Record<string, string | number | boolean> {
    const raw = {
      name: this.name(),
      minPrice: this.minPrice(),
      maxPrice: this.maxPrice(),
      minStock: this.minStock(),
      maxStock: this.maxStock(),
      sort: this.sort(),
      page: this.currentPage(),
      pageSize: this.pageSize(),
    };

    return Object.fromEntries(Object.entries(raw).filter(([, v]) => v !== undefined)) as Record<
      string,
      string | number | boolean
    >;
  }
  readonly pagedResult = httpResource<PagedResult<Product>>(() => ({
    url: 'products',
    params: this.buildParams(),
  }));

  readonly products = computed(() => {
    return this.pagedResult.hasValue() ? this.pagedResult.value().items : [];
  });

  readonly total = computed(() => {
    return this.pagedResult.hasValue() ? this.pagedResult.value().total : 0;
  });
  readonly totalPages = computed(() => {
    return this.pagedResult.hasValue() ? this.pagedResult.value().totalPages : 0;
  });
  readonly hasPreviousPage = computed(() => {
    return this.pagedResult.hasValue() ? this.pagedResult.value().hasPreviousPage : false;
  });
  readonly hasNextPage = computed(() => {
    return this.pagedResult.hasValue() ? this.pagedResult.value().hasNextPage : false;
  });

  readonly lowerLimit = computed(() => (this.currentPage() - 1) * this.pageSize() + 1);
  readonly upperLimit = computed(() => this.lowerLimit() + this.products().length - 1);

  setSelectedPage(page: number): void {
    this.currentPage.set(page);
  }

  setSelectedPageSize(pageSize: number): void {
    this.pageSize.set(pageSize);
    this.currentPage.set(1);
  }

  setName(name: string): void {
    // Bos ya da yalnizca bosluk iceren metin bir filtre degildir.
    this.name.set(name.trim() === '' ? undefined : name.trim());
    this.currentPage.set(1);
  }

  setMinPrice(minPrice: number): void {
    // <input type="number"> bosaltilinca NaN uretir; 0 ise gecerli bir filtredir
    // (maxStock=0 -> tukenmis urunler), o yuzden yalnizca NaN eleniyor.
    this.minPrice.set(Number.isNaN(minPrice) ? undefined : minPrice);
    this.currentPage.set(1);
  }

  setMaxPrice(maxPrice: number): void {
    this.maxPrice.set(Number.isNaN(maxPrice) ? undefined : maxPrice);
    this.currentPage.set(1);
  }

  setMinStock(minStock: number): void {
    this.minStock.set(Number.isNaN(minStock) ? undefined : minStock);
    this.currentPage.set(1);
  }

  setMaxStock(maxStock: number): void {
    this.maxStock.set(Number.isNaN(maxStock) ? undefined : maxStock);
    this.currentPage.set(1);
  }

  setSelectedSort(sort: string): void {
    this.sort.set(sort.trim() === '' ? undefined : sort.trim());
    this.currentPage.set(1);
  }

  resetFilters(): void {
    this.currentPage.set(1);
    this.pageSize.set(5);
    this.name.set(undefined);
    this.minPrice.set(undefined);
    this.maxPrice.set(undefined);
    this.minStock.set(undefined);
    this.maxStock.set(undefined);
    this.sort.set(undefined);
  }

  getById(id: number): Observable<Product> {
    return this.httpClient.get<Product>(`products/${id}`);
  }

  add(name: string, category: string, price: number, stock: number): Observable<Product> {
    return this.httpClient
      .post<Product>('products', { name, category, price, stock })
      .pipe(tap(() => this.pagedResult.reload()));
  }

  update(
    id: number,
    name: string,
    category: string,
    price: number,
    stock: number,
  ): Observable<Product> {
    return this.httpClient
      .put<Product>(`products/${id}`, { name, category, price, stock })
      .pipe(tap(() => this.pagedResult.reload()));
  }

  delete(id: number): Observable<void> {
    return this.httpClient
      .delete<void>(`products/${id}`)
      .pipe(tap(() => this.pagedResult.reload()));
  }
}
