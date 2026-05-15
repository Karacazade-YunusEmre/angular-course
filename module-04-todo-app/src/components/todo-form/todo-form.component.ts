import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { TodoService } from '../../services/todo.service';

@Component({
  selector: 'app-todo-form',
  imports: [],
  templateUrl: './todo-form.component.html',
  styleUrl: './todo-form.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoFormComponent {
  private readonly todoService = inject(TodoService);

  priorities = this.todoService.priorities.asReadonly();

  title = signal('');

  onInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    if (!target) return;

    this.title.set(target.value);
  }

  onsubmit(): void {
    if (this.title() === '' || this.title() === ' ') return;

    this.todoService.add({
      title: this.title(),
      completed: false,
      priority: 'low',
    });

    this.title.set('');
  }
}
