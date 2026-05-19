import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { Priority, Todo, ToggleTodoInput } from '../../models/todo.model';

@Component({
  selector: 'app-todo-item',
  imports: [],
  templateUrl: './todo-item.component.html',
  styleUrl: './todo-item.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoItemComponent {
  todo = input.required<Todo>();
  toggleTodo = output<ToggleTodoInput>();
  deleteTodo = output<string>();

  getPriorityClass(priority: Priority): string {
    return `priority-${priority}`;
  }

  onChange(event: Event, id: string): void {
    const target = event.target as HTMLInputElement;

    this.toggleTodo.emit({ id: id, completed: target.checked });
  }

  deleteTodoEvent(id: string): void {
    this.deleteTodo.emit(id);
  }
}
