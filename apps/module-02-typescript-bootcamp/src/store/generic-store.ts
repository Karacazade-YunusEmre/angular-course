/**
 * ============================================================================
 * GENERIC STORE (Modül 2.2 - Generics)
 * ============================================================================
 * Herhangi bir entity tipini saklayabilen generic store.
 *
 * Bu dosyada Modül 2.2'deki şu konuları görüyoruz:
 * - Generic class: Store<T>
 * - Generic constraint: T extends Identifiable
 * - Generic interface: Identifiable
 *
 * MENTAL MODEL:
 * Store<Todo> dediğinde, T = Todo olur. Tüm metodlar
 * type-safe şekilde Todo bekler ve döner.
 */

// ============================================================================
// Constraint Interface (Modül 2.2)
// ============================================================================

/**
 * Store'a konulan item'ların id'si olmalı.
 *
 * Store<T extends Identifiable> constraint'i ile bunu zorluyoruz.
 * id olmadan getById, update, delete çalışamazdı.
 */
export interface Identifiable {
  id: string;
}

// ============================================================================
// Generic Store Class (Modül 2.2)
// ============================================================================

/**
 * Type-safe, in-memory store.
 *
 * Özellikler:
 * - CRUD işlemleri (add, getById, update, delete)
 * - Immutable update (her zaman yeni array)
 * - Subscribe pattern (publish-subscribe)
 * - Generic — her entity için kullanılabilir
 */
export class Store<T extends Identifiable> {
  private items: T[] = [];
  private listeners: Set<() => void> = new Set();

  // ==========================================================================
  // Subscribe Pattern (Observer)
  // ==========================================================================

  /**
   * State değiştiğinde çağrılacak listener ekler.
   * Unsubscribe fonksiyonu döner — listener'ı kaldırmak için.
   */
  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * Tüm subscriber'lara değişikliği bildir.
   * private — sadece store kendisi tetikleyebilir.
   */
  private notify(): void {
    this.listeners.forEach(listener => listener());
  }

  // ==========================================================================
  // Read Operations
  // ==========================================================================

  /**
   * Tüm item'ları döner (readonly).
   *
   * readonly T[] dönüyoruz çünkü dışarıdan mutate edilmesin istiyoruz.
   * Modül 2.4'te readonly utility'yi öğrendik.
   */
  getAll(): readonly T[] {
    return this.items;
  }

  /**
   * id'ye göre tek item bul.
   *
   * T | undefined dönüyor çünkü bulunmayabilir.
   */
  getById(id: string): T | undefined {
    return this.items.find(item => item.id === id);
  }

  /**
   * Toplam item sayısı.
   */
  get count(): number {
    return this.items.length;
  }

  // ==========================================================================
  // Write Operations (Immutable)
  // ==========================================================================

  /**
   * Yeni item ekler.
   * Immutable: yeni array oluşturur, mevcut array'i mutate etmez.
   */
  add(item: T): void {
    this.items = [...this.items, item];
    this.notify();
  }

  /**
   * Item'ı günceller.
   *
   * changes: Partial<T> — sadece değişen alanları al (Modül 2.4)
   * Return: Güncellenen item veya null (bulunamadıysa)
   */
  update(id: string, changes: Partial<T>): T | null {
    const index = this.items.findIndex(item => item.id === id);
    if (index === -1) return null;

    // Yeni array oluştur, immutable update
    const existingItem = this.items[index]!;
    const updatedItem: T = { ...existingItem, ...changes };

    this.items = [
      ...this.items.slice(0, index),
      updatedItem,
      ...this.items.slice(index + 1)
    ];

    this.notify();
    return updatedItem;
  }

  /**
   * Item'ı siler.
   * Return: Silindi mi? (boolean)
   */
  delete(id: string): boolean {
    const initialLength = this.items.length;
    this.items = this.items.filter(item => item.id !== id);
    const wasDeleted = this.items.length < initialLength;

    if (wasDeleted) {
      this.notify();
    }
    return wasDeleted;
  }

  /**
   * Tüm item'ları temizle.
   */
  clear(): void {
    if (this.items.length === 0) return;
    this.items = [];
    this.notify();
  }

  /**
   * Birden fazla id'yi sil.
   * Return: Silinen sayısı.
   */
  deleteMany(ids: string[]): number {
    const idsSet = new Set(ids);
    const initialLength = this.items.length;
    this.items = this.items.filter(item => !idsSet.has(item.id));
    const deletedCount = initialLength - this.items.length;

    if (deletedCount > 0) {
      this.notify();
    }
    return deletedCount;
  }

  // ==========================================================================
  // Bulk Initialization (LocalStorage'dan yükleme için)
  // ==========================================================================

  /**
   * Mevcut item'ları sıfırlayıp yenilerle değiştirir.
   * Genelde uygulamaya başlarken localStorage'dan yükleme için.
   */
  loadAll(items: T[]): void {
    this.items = [...items];
    this.notify();
  }
}
