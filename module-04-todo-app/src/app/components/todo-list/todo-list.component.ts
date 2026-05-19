import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { Priority, Todo, ToggleTodoInput } from '../../models/todo.model';
import { TodoItemComponent } from '../todo-item/todo-item.component';

@Component({
  selector: 'app-todo-list',
  imports: [TodoItemComponent],
  templateUrl: './todo-list.component.html',
  styleUrl: './todo-list.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoListComponent {
  todos = input.required<Todo[]>();
  toggleTodo = output<ToggleTodoInput>();
  deleteTodo = output<string>();

  protected onToggleTodo($event: ToggleTodoInput) {
    this.toggleTodo.emit($event);
  }

  protected onDeleteTodo($event: string) {
    this.deleteTodo.emit($event);
  }
}
