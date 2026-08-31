/**
 * ============================================================================
 * TODO SERVICE
 * ============================================================================
 * Todo entity'sine özel business logic.
 *
 * Generic Store'u extend ederek Todo özelinde metodlar ekliyoruz.
 *
 * Modül 2'deki şu konuları kullanıyoruz:
 * - Modül 2.1: interface, optional, union types
 * - Modül 2.2: Generic class extension (Store<Todo>)
 * - Modül 2.4: Partial, Omit, Record utility types
 * - Modül 2.5: Type guards (isTodo), narrowing
 */

import { Store } from '../store/generic-store.js';
import { isTodoArray, assertNever } from '../utils/type-guards.js';
import type {
  Todo,
  CreateTodoInput,
  UpdateTodoInput,
  TodoFilters,
  SortOptions,
  TodoStats,
  Priority,
} from '../types/todo.js';

export class TodoService extends Store<Todo> {
  private static readonly STORAGE_KEY = 'todos';

  constructor() {
    super();
    this.loadFromStorage();
  }

  // ==========================================================================
  // Create
  // ==========================================================================

  /**
   * Yeni todo oluşturur.
   *
   * Input: CreateTodoInput — Omit<Todo, 'id' | 'createdAt' | 'updatedAt'>
   * Çıkardığımız alanlar burada otomatik oluşturuluyor.
   */
  createTodo(input: CreateTodoInput): Todo {
    const now = new Date();

    const todo: Todo = {
      id: this.generateId(),
      ...input,
      createdAt: now,
      updatedAt: now,
    };

    this.add(todo);
    this.saveToStorage();
    return todo;
  }

  /**
   * Unique ID üretir.
   *
   * crypto.randomUUID() Node 19+ ve modern tarayıcılarda var.
   * Fallback olarak timestamp + random kullanıyoruz.
   */
  private generateId(): string {
    if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
      return crypto.randomUUID();
    }
    return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  }

  // ==========================================================================
  // Update
  // ==========================================================================

  /**
   * Todo'yu günceller.
   *
   * Input: UpdateTodoInput — Partial<Omit<Todo, 'id' | 'createdAt'>>
   * Yani id ve createdAt değiştirilemez, geri kalanlar opsiyonel.
   */
  updateTodo(id: string, changes: UpdateTodoInput): Todo | null {
    const result = this.update(id, {
      ...changes,
      updatedAt: new Date(),
    });

    if (result) {
      this.saveToStorage();
    }
    return result;
  }

  /**
   * Todo'nun completed durumunu tersine çevirir.
   */
  toggleCompleted(id: string): Todo | null {
    const todo = this.getById(id);
    if (!todo) return null;

    return this.updateTodo(id, { completed: !todo.completed });
  }

  // ==========================================================================
  // Delete
  // ==========================================================================

  /**
   * Todo'yu siler.
   */
  removeTodo(id: string): boolean {
    const result = this.delete(id);
    if (result) {
      this.saveToStorage();
    }
    return result;
  }

  /**
   * Tamamlanmış todoları siler.
   * Return: Silinen sayısı.
   */
  clearCompleted(): number {
    const completedIds = this.getAll()
      .filter(todo => todo.completed)
      .map(todo => todo.id);

    const deletedCount = this.deleteMany(completedIds);
    if (deletedCount > 0) {
      this.saveToStorage();
    }
    return deletedCount;
  }

  // ==========================================================================
  // Bulk Operations
  // ==========================================================================

  /**
   * Tüm todoları tamamlandı olarak işaretle.
   */
  markAllCompleted(): number {
    const incompleteTodos = this.getAll().filter(t => !t.completed);
    let count = 0;

    incompleteTodos.forEach(todo => {
      this.update(todo.id, {
        completed: true,
        updatedAt: new Date(),
      });
      count++;
    });

    if (count > 0) {
      this.saveToStorage();
    }
    return count;
  }

  // ==========================================================================
  // Filter & Sort
  // ==========================================================================

  /**
   * Todo'ları filtreler.
   *
   * Modül 2.5'teki narrowing'i kullanıyoruz:
   * - filters.mode === 'completed' → boolean kontrolü
   * - filters.searchQuery → optional, undefined kontrolü
   */
  filter(filters: TodoFilters): Todo[] {
    return this.getAll().filter(todo => {
      // 1. Mode filter (discriminated union narrowing - Modül 2.5)
      switch (filters.mode) {
        case 'all':
          // Tüm todo'lar geçer
          break;
        case 'active':
          if (todo.completed) return false;
          break;
        case 'completed':
          if (!todo.completed) return false;
          break;
        default:
          // Exhaustive check - yeni mode eklenirse compile error (Modül 2.5)
          return assertNever(filters.mode);
      }

      // 2. Priority filter (optional)
      if (filters.priority && todo.priority !== filters.priority) {
        return false;
      }

      // 3. Search query filter (optional + narrowing)
      if (filters.searchQuery) {
        const query = filters.searchQuery.toLowerCase();
        const titleMatch = todo.title.toLowerCase().includes(query);

        // description optional — narrowing ile güvenli erişim
        const descMatch = todo.description
          ? todo.description.toLowerCase().includes(query)
          : false;

        if (!titleMatch && !descMatch) return false;
      }

      return true;
    });
  }

  /**
   * Todo'ları sıralar.
   */
  sort(options: SortOptions): Todo[] {
    const sorted = [...this.getAll()];

    sorted.sort((a, b) => {
      let comparison = 0;

      switch (options.by) {
        case 'createdAt':
        case 'updatedAt': {
          const aDate = a[options.by].getTime();
          const bDate = b[options.by].getTime();
          comparison = aDate - bDate;
          break;
        }
        case 'priority': {
          // Priority'leri sayısal değere çevir
          const priorityOrder: Record<Priority, number> = {
            low: 1,
            medium: 2,
            high: 3,
          };
          comparison = priorityOrder[a.priority] - priorityOrder[b.priority];
          break;
        }
        case 'title':
          comparison = a.title.localeCompare(b.title);
          break;
        default:
          return assertNever(options.by);
      }

      return options.order === 'asc' ? comparison : -comparison;
    });

    return sorted;
  }

  // ==========================================================================
  // Statistics
  // ==========================================================================

  /**
   * Todo istatistiklerini hesaplar.
   *
   * Return: TodoStats — Record<Priority, number> içerir (Modül 2.4).
   */
  getStats(): TodoStats {
    const all = this.getAll();
    const active = all.filter(t => !t.completed).length;
    const completed = all.length - active;

    // Record başlangıç değeri (Modül 2.4)
    const byPriority: Record<Priority, number> = {
      low: 0,
      medium: 0,
      high: 0,
    };

    all.forEach(todo => {
      byPriority[todo.priority]++;
    });

    return {
      total: all.length,
      active,
      completed,
      byPriority,
    };
  }

  // ==========================================================================
  // Persistence (LocalStorage)
  // ==========================================================================

  /**
   * Mevcut todoları localStorage'a kaydeder.
   */
  private saveToStorage(): void {
    if (typeof localStorage === 'undefined') return; // Node.js'te yok

    try {
      const serialized = JSON.stringify(this.getAll());
      localStorage.setItem(TodoService.STORAGE_KEY, serialized);
    } catch (error) {
      console.error('Failed to save todos to storage:', error);
    }
  }

  /**
   * localStorage'dan todoları yükler.
   *
   * Burada Modül 2.5'teki type guard pattern'i kritik:
   * - JSON.parse → unknown döner
   * - isTodoArray() ile validation
   * - Geçersiz veriler dışlanır
   */
  private loadFromStorage(): void {
    if (typeof localStorage === 'undefined') return; // Node.js'te yok

    const data = localStorage.getItem(TodoService.STORAGE_KEY);
    if (!data) return;

    try {
      const parsed: unknown = JSON.parse(data);

      // Type guard ile validation (Modül 2.5)
      if (!isTodoArray(parsed)) {
        console.warn('Invalid data in storage, ignoring.');
        return;
      }

      // Date string'leri Date objesine çevir
      const todos: Todo[] = parsed.map(todo => ({
        ...todo,
        createdAt: new Date(todo.createdAt),
        updatedAt: new Date(todo.updatedAt),
      }));

      this.loadAll(todos);
    } catch (error) {
      console.error('Failed to load todos from storage:', error);
    }
  }
}
