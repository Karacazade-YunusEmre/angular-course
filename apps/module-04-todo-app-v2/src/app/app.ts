import { Component, computed, inject } from '@angular/core';
import { TodoService } from './services/todo-service';
import { TaskInput } from './components/task-input/task-input';

@Component({
  selector: 'app-root',
  imports: [TaskInput],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  private readonly todoService = inject(TodoService);

  protected readonly todos = this.todoService.todos;

  protected remainingTodos = computed(() => {
    return this.todos().filter((todo) => !todo.completed).length;
  });

  protected addTodo(value: string): void {
    this.todoService.add({
      title: value,
    });
  }

  protected toggleChange(id: string): void {
    this.todoService.toggle(id);
  }

  protected deleteTodo(id: string): void {
    this.todoService.delete(id);
  }
}
