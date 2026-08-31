import { Component, computed, inject, signal } from '@angular/core';
import { ProductService } from '@app/services/product-service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  imports: [],
  selector: 'app-product-form',
  styleUrl: './product-form.scss',
  templateUrl: './product-form.html',
})
export class ProductForm {
  private readonly productService = inject(ProductService);

  protected readonly name = signal('');
  protected readonly category = signal('');
  protected readonly price = signal<number | null>(null);
  protected readonly stock = signal<number | null>(null);

  protected readonly saving = signal(false);
  protected readonly errorMessage = signal<string | null>(null);

  // API'nin doğrulama kuralları: ad 2-120 karakter, kategori zorunlu,
  // fiyat > 0, stok >= 0. Buton bunlar sağlanmadan etkinleşmiyor.
  protected readonly canSubmit = computed(() => {
    const price = this.price();
    const stock = this.stock();

    return (
      !this.saving() &&
      this.name().trim().length >= 2 &&
      this.category().trim().length > 0 &&
      price !== null &&
      price > 0 &&
      stock !== null &&
      stock >= 0
    );
  });

  protected onName(value: string): void {
    this.name.set(value);
  }

  protected onCategory(value: string): void {
    this.category.set(value);
  }

  protected onPrice(value: string): void {
    this.price.set(value === '' ? null : Number(value));
  }

  protected onStock(value: string): void {
    this.stock.set(value === '' ? null : Number(value));
  }

  protected submit(): void {
    if (!this.canSubmit()) return;

    this.saving.set(true);
    this.errorMessage.set(null);

    this.productService
      .add(this.name().trim(), this.category().trim(), this.price()!, this.stock()!)
      .subscribe({
        next: () => {
          this.saving.set(false);
          this.reset();
        },
        error: (error: HttpErrorResponse) => {
          this.saving.set(false);
          // API hataları ProblemDetails formatında döner:
          // { title, status, errors?: { alan: [mesaj] } }
          const problem = error.error;
          const fieldErrors = problem?.errors
            ? Object.values(problem.errors as Record<string, string[]>).flat()
            : [];

          this.errorMessage.set(
            fieldErrors[0] ?? problem?.title ?? 'Ürün eklenemedi, lütfen tekrar dene.',
          );
        },
      });
  }

  private reset(): void {
    this.name.set('');
    this.category.set('');
    this.price.set(null);
    this.stock.set(null);
  }
}
