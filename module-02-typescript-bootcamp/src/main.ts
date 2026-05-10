/**
 * ============================================================================
 * MAIN — KULLANIM ÖRNEKLERİ
 * ============================================================================
 * Bu dosya TodoService'i nasıl kullanacağını gösterir.
 *
 * Çalıştırmak için:
 *   npm run build
 *   npm start
 */

import { TodoService } from './services/todo.service.js';
import type {
  CreateTodoInput,
  UpdateTodoInput,
  TodoFilters,
} from './types/todo.js';

// ============================================================================
// Helper: Konsol başlık yazdırma
// ============================================================================

function section(title: string): void {
  console.log('\n' + '='.repeat(60));
  console.log(`  ${title}`);
  console.log('='.repeat(60));
}

// ============================================================================
// DEMO BAŞLIYOR
// ============================================================================

section('1. SERVICE OLUŞTURMA');

const todos = new TodoService();
console.log('✓ TodoService oluşturuldu');
console.log(`  Mevcut todo sayısı: ${todos.count}`);

// ============================================================================
// SUBSCRIBE - State değişikliklerini dinle
// ============================================================================

section('2. SUBSCRIBE PATTERN');

let changeCount = 0;
const unsubscribe = todos.subscribe(() => {
  changeCount++;
  console.log(`  📢 State değişti! (toplam: ${changeCount} kez)`);
});

console.log('✓ Listener kaydedildi');

// ============================================================================
// CREATE - Yeni todolar oluştur
// ============================================================================

section('3. TODO OLUŞTURMA');

// TypeScript bizi koruyor:
// - id, createdAt, updatedAt veremeyiz (Omit ile çıkarıldı)
// - priority sadece 'low' | 'medium' | 'high' olabilir (union type)

const todo1Input: CreateTodoInput = {
  title: 'TypeScript öğren',
  description: 'Modül 2 bitti, tüm konseptleri kavradım',
  completed: false,
  priority: 'high',
};

const todo1 = todos.createTodo(todo1Input);
console.log('✓ Todo 1 oluşturuldu:');
console.log(`  id: ${todo1.id}`);
console.log(`  title: ${todo1.title}`);

const todo2 = todos.createTodo({
  title: 'Angular Modül 3\'e başla',
  completed: false,
  priority: 'medium',
});
console.log(`✓ Todo 2 oluşturuldu: ${todo2.title}`);

const todo3 = todos.createTodo({
  title: 'Counter App yap',
  description: 'Modül 3.7\'deki mini proje',
  completed: false,
  priority: 'medium',
});
console.log(`✓ Todo 3 oluşturuldu: ${todo3.title}`);

const todo4 = todos.createTodo({
  title: 'Kahve iç',
  completed: true,
  priority: 'low',
});
console.log(`✓ Todo 4 oluşturuldu: ${todo4.title} (tamamlandı)`);

// ============================================================================
// READ - Todoları oku
// ============================================================================

section('4. TODO OKUMA');

console.log(`Toplam todo: ${todos.count}`);

const allTodos = todos.getAll();
console.log('\nTüm todolar:');
allTodos.forEach((t, i) => {
  const mark = t.completed ? '✓' : '○';
  console.log(`  ${i + 1}. ${mark} [${t.priority}] ${t.title}`);
});

// getById
const found = todos.getById(todo1.id);
console.log(`\ngetById(${todo1.id.substring(0, 8)}...):`);
console.log(`  ${found ? '✓ Bulundu: ' + found.title : '✗ Bulunamadı'}`);

// ============================================================================
// UPDATE - Todo güncelleme
// ============================================================================

section('5. TODO GÜNCELLEME');

// Partial<Omit<...>> sayesinde sadece değiştirmek istediğimizi gönderiyoruz
const updateInput: UpdateTodoInput = {
  description: 'Modül 2 bitti — Modül 3 başlıyor!',
  priority: 'high',
};

const updated = todos.updateTodo(todo2.id, updateInput);
console.log('✓ Todo 2 güncellendi:');
console.log(`  Yeni description: ${updated?.description}`);
console.log(`  Yeni priority: ${updated?.priority}`);

// Toggle completed
todos.toggleCompleted(todo1.id);
console.log(`✓ Todo 1 toggle edildi`);

const todo1Updated = todos.getById(todo1.id);
console.log(`  Yeni completed durumu: ${todo1Updated?.completed}`);

// ============================================================================
// FILTER - Filtreleme (Modül 2.5 narrowing)
// ============================================================================

section('6. FİLTRELEME');

// Filtre 1: Sadece aktif olanlar
const activeFilter: TodoFilters = { mode: 'active' };
const activeTodos = todos.filter(activeFilter);
console.log(`Aktif todolar (${activeTodos.length}):`);
activeTodos.forEach(t => console.log(`  ○ ${t.title}`));

// Filtre 2: Sadece tamamlananlar
const completedTodos = todos.filter({ mode: 'completed' });
console.log(`\nTamamlanan todolar (${completedTodos.length}):`);
completedTodos.forEach(t => console.log(`  ✓ ${t.title}`));

// Filtre 3: High priority + active
const highPriorityActive = todos.filter({
  mode: 'active',
  priority: 'high',
});
console.log(`\nYüksek öncelikli + aktif (${highPriorityActive.length}):`);
highPriorityActive.forEach(t => console.log(`  ! ${t.title}`));

// Filtre 4: Search query
const searchResults = todos.filter({
  mode: 'all',
  searchQuery: 'angular',
});
console.log(`\n"angular" araması (${searchResults.length}):`);
searchResults.forEach(t => console.log(`  🔍 ${t.title}`));

// ============================================================================
// SORT - Sıralama
// ============================================================================

section('7. SIRALAMA');

const sortedByPriority = todos.sort({ by: 'priority', order: 'desc' });
console.log('Önceliğe göre (yüksekten düşüğe):');
sortedByPriority.forEach(t => {
  console.log(`  [${t.priority.padEnd(6)}] ${t.title}`);
});

const sortedByTitle = todos.sort({ by: 'title', order: 'asc' });
console.log('\nBaşlığa göre (A→Z):');
sortedByTitle.forEach(t => console.log(`  ${t.title}`));

// ============================================================================
// STATISTICS - İstatistikler
// ============================================================================

section('8. İSTATİSTİKLER');

const stats = todos.getStats();
console.log(`Toplam:      ${stats.total}`);
console.log(`Aktif:       ${stats.active}`);
console.log(`Tamamlanan:  ${stats.completed}`);
console.log(`\nÖncelik dağılımı:`);
console.log(`  High:    ${stats.byPriority.high}`);
console.log(`  Medium:  ${stats.byPriority.medium}`);
console.log(`  Low:     ${stats.byPriority.low}`);

// ============================================================================
// TYPESCRIPT KORUMASI — Neler engelleniyor?
// ============================================================================

section('9. TYPESCRIPT KORUMASI (Yorumlu örnekler)');

console.log('Aşağıdaki kullanımlar TypeScript tarafından engellenir:');
console.log('');
console.log('  // ✗ Error: completed eksik');
console.log("  todos.createTodo({ title: 'X', priority: 'high' });");
console.log('');
console.log('  // ✗ Error: \'urgent\' Priority union\'da yok');
console.log("  todos.createTodo({ title: 'X', priority: 'urgent', ... });");
console.log('');
console.log('  // ✗ Error: id readonly, güncellenemez');
console.log("  todos.updateTodo(id, { id: 'newId' });");
console.log('');
console.log('  // ✗ Error: completed boolean olmalı');
console.log("  todos.updateTodo(id, { completed: 'yes' });");
console.log('');
console.log('  // ✗ Error: priority\'de typo, autocomplete yardımcı olur');
console.log("  todos.filter({ mode: 'all', priorty: 'high' });");

// ============================================================================
// CLEANUP
// ============================================================================

section('10. CLEANUP');

unsubscribe();
console.log('✓ Listener kaldırıldı');

// Tamamlananları temizle
const cleared = todos.clearCompleted();
console.log(`✓ ${cleared} tamamlanmış todo silindi`);

console.log(`\nKalan todo sayısı: ${todos.count}`);

section('DEMO TAMAMLANDI 🎉');

console.log(`
Bu demo'da Modül 2'nin tüm konseptlerini kullandık:
- M2.1: interfaces, union types, optional, readonly
- M2.2: Generics (Store<T>, T extends Identifiable)
- M2.3: Decorators (kavramsal — burada yok ama domain bilgi)
- M2.4: Partial, Omit, Record utility types
- M2.5: Type guards (isTodo), narrowing, assertNever

Sıradaki adım: Modül 3 — Angular'a giriş! 🚀
`);
