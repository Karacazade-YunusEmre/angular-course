import { ChangeDetectionStrategy, Component, input, output, signal } from '@angular/core';
import { Priority, Todo, UpdateTodoInput } from '../../models/todo.model';

@Component({
  selector: 'app-todo-item',
  imports: [],
  templateUrl: './todo-item.component.html',
  styleUrl: './todo-item.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoItemComponent {
  todo = input.required<Todo>();
  toggleTodo = output<string>();
  deleteTodo = output<string>();
  updateTodo = output<UpdateTodoInput>();

  isEditing = signal(false);
  editText = signal('');

  protected getPriorityClass(priority: Priority): string {
    return `priority-${priority}`;
  }

  protected onChange(id: string): void {
    this.toggleTodo.emit(id);
  }

  protected deleteTodoEvent(id: string): void {
    this.deleteTodo.emit(id);
  }

  protected onEditInput($event: Event) {
    const target = $event.target as HTMLInputElement;
    this.editText.set(target.value);
  }

  protected onEditEnter() {
    const trimmedText = this.editText().trim();
    if (trimmedText.length === 0) return;
    if (trimmedText === this.todo().title) {
      this.isEditing.set(false);
      return;
    }

    this.updateTodo.emit({
      id: this.todo().id,
      title: trimmedText,
    });
    this.isEditing.set(false);
  }

  protected cancelEdit() {
    this.isEditing.set(false);
  }

  protected startEditMode() {
    this.editText.set(this.todo().title);
    this.isEditing.set(true);
  }
}
