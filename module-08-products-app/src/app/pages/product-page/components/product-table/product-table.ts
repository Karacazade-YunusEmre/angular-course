import { Component, computed, inject } from '@angular/core';
import { CurrencyPipe } from '@angular/common';
import { ProductService } from '@app/services/product-service';
import { Product } from '@app/models/product';

@Component({
  imports: [CurrencyPipe],
  selector: 'app-product-table',
  styleUrl: './product-table.scss',
  templateUrl: './product-table.html',
})
export class ProductTable {
  private readonly productService = inject(ProductService);

  protected readonly isLoading = this.productService.pagedResult.isLoading;
  protected readonly error = this.productService.pagedResult.error;
  protected readonly products = this.productService.products;

  protected readonly total = this.productService.total;
  protected readonly totalPages = this.productService.totalPages;
  protected readonly hasPreviousPage = this.productService.hasPreviousPage;
  protected readonly hasNextPage = this.productService.hasNextPage;

  protected readonly currentPage = this.productService.currentPage;
  protected readonly pageSize = this.productService.pageSize;
  protected readonly lowerLimit = this.productService.lowerLimit;
  protected readonly upperLimit = this.productService.upperLimit;

  protected readonly pageSizeOptions = [5, 10, 20, 50];

  /**
   * Sayfa numarası butonları. Sayfa sayısı fazlaysa araya '…' konur:
   * [1, '…', 22, 23, 24, 25, 26, '…', 48]
   */
  protected readonly pageNumbers = computed<(number | '…')[]>(() => {
    const total = this.totalPages();
    const current = this.currentPage();

    if (total <= 7) {
      return Array.from({ length: total }, (_, i) => i + 1);
    }

    const pages: (number | '…')[] = [1];
    const start = Math.max(2, current - 2);
    const end = Math.min(total - 1, current + 2);

    if (start > 2) pages.push('…');
    for (let page = start; page <= end; page++) pages.push(page);
    if (end < total - 1) pages.push('…');
    pages.push(total);

    return pages;
  });

  protected goToPage(page: number): void {
    this.productService.setSelectedPage(page);
  }

  protected previousPage(): void {
    if (this.hasPreviousPage()) this.goToPage(this.currentPage() - 1);
  }

  protected nextPage(): void {
    if (this.hasNextPage()) this.goToPage(this.currentPage() + 1);
  }

  protected onPageSize(value: string): void {
    this.productService.setSelectedPageSize(Number(value));
  }

  protected retry(): void {
    this.productService.pagedResult.reload();
  }

  protected remove(product: Product): void {
    if (!confirm(`"${product.name}" silinsin mi?`)) return;

    // Sayfadaki son ürünse ve ilk sayfada değilsek bir önceki sayfaya dön,
    // yoksa kullanıcı boş bir sayfada kalır.
    const wasLastOnPage = this.products().length === 1 && this.currentPage() > 1;

    this.productService.delete(product.id).subscribe({
      next: () => {
        if (wasLastOnPage) this.goToPage(this.currentPage() - 1);
      },
      error: () => alert('Ürün silinemedi.'),
    });
  }

  /** Stok rozetinin rengi: 0 → tükendi, 1-20 → az, üstü → bol. */
  protected stockClass(stock: number): string {
    if (stock === 0) return 'stock-out';
    if (stock <= 20) return 'stock-low';
    return 'stock-ok';
  }
}
