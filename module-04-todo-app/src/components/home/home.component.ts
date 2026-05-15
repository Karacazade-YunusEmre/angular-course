import { ChangeDetectionStrategy, Component, inject, OnInit, signal } from '@angular/core';
import { TodoService } from '../../services/todo.service';
import { Todo } from '../../models/todo.model';
import { HeaderComponent } from '../header/header.component';
import { TodoFormComponent } from '../todo-form/todo-form.component';
import { TodoFilterComponent } from '../todo-filter/todo-filter.component';
import { TodoListComponent } from '../todo-list/todo-list.component';
import { FooterComponent } from '../footer/footer.component';

@Component({
  selector: 'app-home',
  imports: [
    HeaderComponent,
    TodoFormComponent,
    TodoFilterComponent,
    TodoListComponent,
    FooterComponent,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomeComponent implements OnInit {
  todos = signal<Todo[]>([]);

  private readonly TodoService = inject(TodoService);

  ngOnInit(): void {
    this.todos.set(this.TodoService.todos());
  }
}
