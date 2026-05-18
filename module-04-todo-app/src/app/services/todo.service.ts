import { Injectable, signal } from '@angular/core';
import {
  CreateTodoInput,
  FilterMode,
  PriorityOption,
  Todo,
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

  static readonly LOCALSTORAGE_TODO_KEY = 'todos';

  constructor() {
    this._todos.set(this.getTodos());
  }

  add(todoInput: CreateTodoInput): void {
    const newTodo: Todo = {
      id: crypto.randomUUID().toLowerCase().toString(),
      ...todoInput,
      createdAt: new Date(),
    };
    this._todos.update((todos) => [...todos, newTodo]);

    this.saveTodos();
  }

  update(id: string, todoInput: UpdateTodoInput): void {
    const currentTodo: Todo | undefined = this._todos().find((t) => t.id === id);
    if (currentTodo === undefined) return;

    this._todos.update((todos) => [
      ...todos.filter((t) => t.id !== id),
      { ...currentTodo, ...todoInput },
    ]);

    this.saveTodos();
  }

  delete(id: string): void {
    this._todos.update((todos) => todos.filter((t) => t.id !== id));
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
