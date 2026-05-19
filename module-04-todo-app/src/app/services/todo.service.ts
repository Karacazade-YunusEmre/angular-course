import { computed, Injectable, signal } from '@angular/core';
import {
  CreateTodoInput,
  FilterMode,
  PriorityOption,
  Todo,
  ToggleTodoInput,
  UpdateTodoInput,
} from '../models/todo.model';

@Injectable({ providedIn: 'root' })
export class TodoService {
  private _todos = signal<Todo[]>([]);
  private _filterMode = signal<FilterMode>('all');

  todos = this._todos.asReadonly();
  filterMode = this._filterMode.asReadonly();
  priorityOptions: PriorityOption[] = [
    { key: 'low', value: 'Low' },
    { key: 'medium', value: 'Medium' },
    { key: 'high', value: 'High' },
  ];

  filteredTodos = computed(() => {
    switch (this.filterMode()) {
      case 'all':
        return this._todos();
      case 'active':
        return this._todos().filter((t) => !t.completed);
      case 'completed':
        return this._todos().filter((t) => t.completed);
      default:
        return this._todos();
    }
  });

  totalCount = computed(() => this.todos().length);
  completedCount = computed(() => this.todos().filter((t) => t.completed).length);
  activeCount = computed(() => this.totalCount() - this.completedCount());

  highCount = computed(() => this.todos().filter((t) => t.priority === 'high').length);
  mediumCount = computed(() => this.todos().filter((t) => t.priority === 'medium').length);
  lowCount = computed(() => this.todos().filter((t) => t.priority === 'low').length);

  static readonly LOCALSTORAGE_TODO_KEY = 'todos';

  constructor() {
    this._todos.set(this.getTodos());
  }

  changeFilterMode(filterMode: FilterMode): void {
    this._filterMode.set(filterMode);
  }

  add(todoInput: CreateTodoInput): void {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      ...todoInput,
      createdAt: new Date(),
    };
    this._todos.update((todos) => [...todos, newTodo]);

    this.saveTodos();
  }

  toggle(toggleInput: ToggleTodoInput): void {
    this._todos.update((todos) =>
      todos.map((todo) =>
        todo.id === toggleInput.id ? { ...todo, completed: toggleInput.completed } : todo,
      ),
    );

    this.saveTodos();
  }

  update(todoInput: UpdateTodoInput): void {
    this._todos.update((todos) =>
      todos.map((todo) => (todo.id === todoInput.id ? { ...todo, title: todoInput.title } : todo)),
    );

    this.saveTodos();
  }

  delete(id: string): void {
    this._todos.update((todos) => todos.filter((t) => t.id !== id));
    this.saveTodos();
  }

  clearCompletedTodos(): void {
    const result = window.confirm('Tamamlanan görevleri silmek istediğinize emin misiniz?');
    if (!result) return;

    this._todos.update((todos) => todos.filter((t) => !t.completed));
    this.saveTodos();
  }

  private getTodos(): Todo[] {
    const storageValues = localStorage.getItem(TodoService.LOCALSTORAGE_TODO_KEY);

    return storageValues ? JSON.parse(storageValues) : [];
  }

  private saveTodos() {
    localStorage.setItem(TodoService.LOCALSTORAGE_TODO_KEY, JSON.stringify(this._todos()));
  }
}
