import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { Todo, UpdateTodoInput } from '../../models/todo.model';
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
  toggleTodo = output<string>();
  deleteTodo = output<string>();
  updateTodo = output<UpdateTodoInput>();

  protected onToggleTodo(id: string) {
    this.toggleTodo.emit(id);
  }

  protected onDeleteTodo($event: string) {
    this.deleteTodo.emit($event);
  }

  protected updateTodoEvent(input: UpdateTodoInput) {
    this.updateTodo.emit(input);
  }
}
