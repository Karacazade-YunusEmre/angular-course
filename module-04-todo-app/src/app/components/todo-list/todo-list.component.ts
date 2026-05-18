import { ChangeDetectionStrategy, Component, computed, input } from '@angular/core';
import { Priority, Todo } from '../../models/todo.model';

@Component({
  selector: 'app-todo-list',
  imports: [],
  templateUrl: './todo-list.component.html',
  styleUrl: './todo-list.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoListComponent {
  todos = input.required<Todo[]>();

  getPriorityClass(priority: Priority): string {
    return `priority-${priority}`;
  }
}
