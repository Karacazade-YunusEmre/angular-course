import { Component, inject } from '@angular/core';
import { FooterComponent } from './components/footer/footer.component';
import { HeaderComponent } from './components/header/header.component';
import { TodoFilterComponent } from './components/todo-filter/todo-filter.component';
import { TodoFormComponent } from './components/todo-form/todo-form.component';
import { TodoListComponent } from './components/todo-list/todo-list.component';
import { TodoService } from './services/todo.service';
import { CreateTodoInput, FilterMode, ToggleTodoInput } from './models/todo.model';
import { TodoStatsComponent } from './components/todo-stats/todo-stats.component';

@Component({
  selector: 'app-root',
  imports: [
    FooterComponent,
    HeaderComponent,
    TodoFilterComponent,
    TodoFormComponent,
    TodoListComponent,
    TodoStatsComponent,
  ],
  templateUrl: 'app.html',
  styleUrl: 'app.scss',
})
export class App {
  private readonly todoService = inject(TodoService);

  todos = this.todoService.filteredTodos;
  priorityOptions = this.todoService.priorityOptions;

  total = this.todoService.totalCount;
  active = this.todoService.activeCount;
  completed = this.todoService.completedCount;

  high = this.todoService.highCount;
  medium = this.todoService.mediumCount;
  low = this.todoService.lowCount;

  activeFilter = this.todoService.filterMode;

  addTodo(todoInput: CreateTodoInput): void {
    this.todoService.add(todoInput);
  }

  toggleTodo(toggleTodo: ToggleTodoInput): void {
    this.todoService.toggle(toggleTodo);
  }

  deleteTodo(id: string): void {
    this.todoService.delete(id);
  }

  changeFilter(filter: FilterMode): void {
    this.todoService.changeFilterMode(filter);
  }

  clearCompletedTodos(): void {
    this.todoService.clearCompletedTodos();
  }
}
