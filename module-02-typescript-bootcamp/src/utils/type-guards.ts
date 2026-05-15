/**
 * ============================================================================
 * TYPE GUARDS (Modül 2.5)
 * ============================================================================
 * Runtime'da tip kontrolü yapan fonksiyonlar.
 *
 * Bu dosyada Modül 2.5'teki şu konuları görüyoruz:
 * - Custom type guards (obj is User pattern)
 * - typeof, instanceof, in operatörleri
 * - Type predicates ile narrowing
 *
 * NEDEN VAR? localStorage'dan veya API'den gelen veriyi
 * "User'mış gibi" davranamayız. Önce kontrol etmeliyiz.
 */

import type { Todo, Priority } from '../types/todo.js';

// ============================================================================
// Priority Type Guard
// ============================================================================

/**
 * Bir değerin geçerli Priority olup olmadığını kontrol eder.
 *
 * `value is Priority` → type predicate (Modül 2.5)
 * Bu fonksiyon true dönerse, TypeScript value'nun Priority olduğunu bilir.
 */
export function isPriority(value: unknown): value is Priority {
  return value === 'low' || value === 'medium' || value === 'high';
}

// ============================================================================
// Todo Type Guard
// ============================================================================

/**
 * Bir object'in geçerli Todo olup olmadığını kontrol eder.
 *
 * Adım adım kontrol:
 * 1. Object mi? (typeof + null check)
 * 2. Gerekli property'ler var mı ve doğru tipte mi?
 * 3. Optional property doğru tipte mi (varsa)?
 *
 * BU PATTERN ÇOK YAYGIN — localStorage, API response, JSON parse
 * gibi her durumda kullanırsın.
 */
export function isTodo(obj: unknown): obj is Todo {
  // 1. Object kontrolü (typeof null === 'object' bug'ını da yakalar)
  if (typeof obj !== 'object' || obj === null) {
    return false;
  }

  // unknown'ı Record<string, unknown>'a cast et — property erişimi için
  const candidate = obj as Record<string, unknown>;

  // 2. Required property kontrolleri
  if (typeof candidate.id !== 'string') return false;
  if (typeof candidate.title !== 'string') return false;
  if (typeof candidate.completed !== 'boolean') return false;
  if (!isPriority(candidate.priority)) return false;

  // 3. Date kontrolü — JSON'dan parse edildiyse string olabilir
  // Burada esnek davranıyoruz: hem Date object hem string kabul ediyoruz
  const createdAtValid =
    candidate.createdAt instanceof Date || typeof candidate.createdAt === 'string';
  const updatedAtValid =
    candidate.updatedAt instanceof Date || typeof candidate.updatedAt === 'string';

  if (!createdAtValid || !updatedAtValid) return false;

  // 4. Optional property kontrolü — varsa string olmalı
  if (candidate.description !== undefined && typeof candidate.description !== 'string') {
    return false;
  }

  return true;
}

// ============================================================================
// Array Type Guard
// ============================================================================

/**
 * Bir array'in tüm elemanlarının Todo olup olmadığını kontrol eder.
 *
 * Modül 2.5'te öğrendiğimiz pattern:
 * .filter(isTodo) ile invalid item'ları otomatik dışlama.
 */
export function isTodoArray(arr: unknown): arr is Todo[] {
  return Array.isArray(arr) && arr.every(isTodo);
}

// ============================================================================
// Generic Helpers (Modül 2.5)
// ============================================================================

/**
 * null ve undefined'ı çıkarır.
 *
 * Kullanım:
 *   const items = ['a', null, 'b', undefined];
 *   const filtered = items.filter(isDefined);  // string[]
 */
export function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

/**
 * Exhaustive check — bir union'da tüm case'lerin işlendiğinden emin olur.
 *
 * Modül 2.5'te öğrendik:
 *   switch (status) {
 *     case 'a': return ...;
 *     case 'b': return ...;
 *     default: return assertNever(status);  // 'c' eklenirse compile error!
 *   }
 */
export function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`);
}
