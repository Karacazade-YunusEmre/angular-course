/**
 * ============================================================================
 * DOMAIN MODELLERİ
 * ============================================================================
 * Bu dosya tüm veri şekillerini (data shapes) tanımlar.
 *
 * Modül 2'deki şu konuları kullanıyoruz:
 * - Modül 2.1: interface, readonly, optional (?), union types
 * - Modül 2.4: Utility types (Omit, Partial)
 */

// ============================================================================
// Union Types (Modül 2.1)
// ============================================================================

/**
 * Todo'nun öncelik seviyesi.
 * Union type ile tip-güvenli enum benzeri yapı.
 */
export type Priority = 'low' | 'medium' | 'high';

/**
 * Filtreleme modu.
 * Discriminated union için kullanılır.
 */
export type FilterMode = 'all' | 'active' | 'completed';

/**
 * Sıralama kriteri.
 */
export type SortBy = 'createdAt' | 'updatedAt' | 'priority' | 'title';
export type SortOrder = 'asc' | 'desc';

// ============================================================================
// Ana Domain Model (Modül 2.1)
// ============================================================================

/**
 * Todo entity'si.
 *
 * Önemli noktalar:
 * - id ve createdAt readonly — değiştirilemez (Modül 2.1)
 * - description optional (?) — olmayabilir (Modül 2.1)
 * - priority union type — sadece belirli değerler (Modül 2.1)
 */
export interface Todo {
  readonly id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: Priority;
  readonly createdAt: Date;
  updatedAt: Date;
}

// ============================================================================
// DTO / Input Types (Modül 2.4 - Utility Types)
// ============================================================================

/**
 * Yeni todo oluştururken gönderilecek payload.
 *
 * Omit<T, K> ile id, createdAt, updatedAt'i çıkardık.
 * Çünkü bunları sistem otomatik üretecek (Modül 2.4).
 */
export type CreateTodoInput = Omit<Todo, 'id' | 'createdAt' | 'updatedAt'>;

/**
 * Todo güncellerken gönderilecek payload.
 *
 * Önce Omit ile id ve createdAt'i çıkardık (değiştirilemez alanlar).
 * Sonra Partial ile geri kalanları optional yaptık (sadece değişenler gönderilsin).
 * Modül 2.4'te utility kombinasyonları gördük.
 */
export type UpdateTodoInput = Partial<Omit<Todo, 'id' | 'createdAt'>>;

// ============================================================================
// Filter Types
// ============================================================================

/**
 * Filtreleme parametreleri.
 * priority ve searchQuery optional çünkü her zaman gerekmez.
 */
export interface TodoFilters {
  mode: FilterMode;
  priority?: Priority;
  searchQuery?: string;
}

/**
 * Sıralama parametreleri.
 */
export interface SortOptions {
  by: SortBy;
  order: SortOrder;
}

// ============================================================================
// Statistics Type (Modül 2.4 - Record)
// ============================================================================

/**
 * Todo istatistikleri.
 *
 * Record<Priority, number> ile priority'lerin her birine
 * bir sayı eşliyoruz: { low: 3, medium: 5, high: 2 }
 * Modül 2.4'te Record utility'yi gördük.
 */
export interface TodoStats {
  total: number;
  active: number;
  completed: number;
  byPriority: Record<Priority, number>;
}
