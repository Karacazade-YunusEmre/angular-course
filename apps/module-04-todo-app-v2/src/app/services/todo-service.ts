import { Service, signal } from '@angular/core';
import { CreateTodoInput, Todo } from '../models/todo';

@Service()
export class TodoService {
  private _todos = signal<Todo[]>([]);

  todos = this._todos.asReadonly();

  add(input: CreateTodoInput): void {
    const newTodo: Todo = {
      id: crypto.randomUUID(),
      ...input,
      completed: false,
    };
    this._todos.update((value) => [...value, newTodo]);
  }

  delete(id: string): void {
    this._todos.update((value) => value.filter((i) => i.id !== id));
  }

  toggle(id: string): void {
    this._todos.update((todos) =>
      todos.map((todo) => (todo.id === id ? { ...todo, completed: !todo.completed } : todo)),
    );
  }
}
