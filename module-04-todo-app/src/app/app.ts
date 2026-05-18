import { Component, inject } from '@angular/core';
import { FooterComponent } from './components/footer/footer.component';
import { HeaderComponent } from './components/header/header.component';
import { TodoFilterComponent } from './components/todo-filter/todo-filter.component';
import { TodoFormComponent } from './components/todo-form/todo-form.component';
import { TodoListComponent } from './components/todo-list/todo-list.component';
import { TodoService } from './services/todo.service';
import { CreateTodoInput } from './models/todo.model';

@Component({
  selector: 'app-root',
  imports: [
    FooterComponent,
    HeaderComponent,
    TodoFilterComponent,
    TodoFormComponent,
    TodoListComponent,
  ],
  templateUrl: 'app.html',
  styleUrl: 'app.scss',
})
export class App {
  private readonly todoService = inject(TodoService);

  todos = this.todoService.todos;
  priorityOptions = this.todoService.priorityOptions;

  addTodo(todoInput: CreateTodoInput): void {
    this.todoService.add(todoInput);
  }
}
