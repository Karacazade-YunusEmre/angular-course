# Modül 2.6 — TypeScript Bootcamp Mini Proje

> **Type-safe ToDo Manager** — Modül 2'de öğrendiklerimizin tamamını birleştiren mini proje.

## 🎯 Proje Hedefi

Bu proje Angular **DEĞİL** — saf TypeScript. Amacımız Modül 2'de öğrendiğimiz TypeScript konseptlerini gerçek bir projede pekiştirmek. Modül 3-4'te aynı projeyi Angular ile yeniden yazıp karşılaştıracağız.

## 📚 Kullanılan Konseptler

| Modül | Konsept | Nerede? |
|-------|---------|---------|
| **2.1** | Interfaces, readonly, optional | `Todo`, `TodoFilters` |
| **2.1** | Union types | `Priority`, `FilterMode`, `SortBy` |
| **2.2** | Generic class | `Store<T>` |
| **2.2** | Generic constraint | `T extends Identifiable` |
| **2.4** | `Omit<T, K>` | `CreateTodoInput` |
| **2.4** | `Partial<T>` | `UpdateTodoInput`, `update()` |
| **2.4** | `Record<K, V>` | `TodoStats.byPriority` |
| **2.4** | `readonly T[]` | `getAll()` return type |
| **2.5** | Custom type guards (`is T`) | `isTodo`, `isPriority`, `isDefined` |
| **2.5** | `typeof`, `instanceof` checks | `isTodo()` içinde |
| **2.5** | Discriminated union narrowing | `filter()` içinde `switch` |
| **2.5** | `assertNever` (exhaustive) | `filter()`, `sort()` default cases |

## 📂 Klasör Yapısı

```
typescript-bootcamp/
├── src/
│   ├── types/
│   │   └── todo.ts              ← Domain modelleri, types
│   ├── store/
│   │   └── generic-store.ts     ← Generic Store<T> class
│   ├── services/
│   │   └── todo.service.ts      ← TodoService (Store<Todo>)
│   ├── utils/
│   │   └── type-guards.ts       ← isTodo, isDefined, assertNever
│   └── main.ts                  ← Kullanım örnekleri (demo)
├── package.json
├── tsconfig.json
└── README.md
```

## 🚀 Kurulum ve Çalıştırma

### 1. Bağımlılıkları yükle

```bash
npm install
```

### 2. Type-check (kod doğru mu?)

```bash
npm run type-check
```

### 3. Derle ve çalıştır

```bash
npm run build
npm start
```

### 4. Watch mode (değişiklikte otomatik derleme)

```bash
npm run dev
```

## 🧪 Kendi Pratiğin

Bu projeyi geliştirmek için 5 öneri:

### Egzersiz 1: Tag/Etiket Sistemi

```typescript
// Todo interface'ine ekle:
interface Todo {
  // ... mevcut alanlar
  tags: readonly string[];  // readonly array!
}

// TodoService'e ekle:
addTag(id: string, tag: string): Todo | null
removeTag(id: string, tag: string): Todo | null
getByTag(tag: string): Todo[]
```

### Egzersiz 2: Undo/Redo

History stack ile undo/redo:

```typescript
class TodoServiceWithHistory extends TodoService {
  private undoStack: Todo[][] = [];
  private redoStack: Todo[][] = [];

  undo(): boolean { /* ... */ }
  redo(): boolean { /* ... */ }
  canUndo(): boolean { /* ... */ }
  canRedo(): boolean { /* ... */ }
}
```

### Egzersiz 3: Due Date

```typescript
interface Todo {
  // ... mevcut alanlar
  dueDate?: Date;  // optional
}

// Yeni metodlar:
getOverdueTodos(): Todo[]
getDueToday(): Todo[]
getDueThisWeek(): Todo[]
```

### Egzersiz 4: Categories

```typescript
type Category = 'work' | 'personal' | 'shopping' | 'health';

interface Todo {
  // ... mevcut alanlar
  category: Category;
}

// Filter'a category ekle, getStats'a categoryDağılımı ekle
```

### Egzersiz 5: Export/Import

```typescript
// JSON olarak export
exportToJson(): string

// JSON'dan import (type guard ile validation!)
importFromJson(json: string): {
  imported: number;
  failed: number;
  errors: string[];
}
```

## 💡 Önemli Notlar

### TypeScript'in Süper Gücü

Bu projede şunları **denersen TypeScript hata verir**:

```typescript
// ✗ Error: completed eksik
todos.createTodo({ title: 'X', priority: 'high' });

// ✗ Error: 'urgent' Priority'de yok
todos.createTodo({ title: 'X', priority: 'urgent', completed: false });

// ✗ Error: id readonly
todos.updateTodo(id, { id: 'newId' });

// ✗ Error: completed boolean olmalı
todos.updateTodo(id, { completed: 'yes' });
```

Bu **compile-time** güvenliktir — kodu çalıştırmadan hatalar yakalanır.

### Type Guards Bağlamı

Modül 2.5'te öğrendiğimiz type guard'lar burada gerçek bir senaryoda kullanılıyor:

```typescript
// loadFromStorage() içinde:
const parsed: unknown = JSON.parse(data);  // unknown — bilmiyoruz

if (!isTodoArray(parsed)) {                // type guard
  return;  // Geçersiz veri, ignore
}

// Bu satırdan sonra parsed: Todo[] (narrowed!)
parsed.map(todo => /* ... */);
```

Bu pattern **API'den veri çekme**, **localStorage**, **JSON parsing** gibi her durumda kullanılır. Gerçek projelerde sürekli karşına çıkacak.

## ➡️ Sıradaki Adım

Bu projeyi anladığın zaman **Modül 3 — İlk Angular Uygulaması**'na geçebilirsin. Orada aynı tipte bir uygulamayı (Counter App) Angular ile yazacağız ve farkları göreceğiz.

🎉 Başarılar!
