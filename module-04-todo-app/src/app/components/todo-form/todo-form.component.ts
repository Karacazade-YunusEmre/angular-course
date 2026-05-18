import { ChangeDetectionStrategy, Component, input, output, signal } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { CreateTodoInput, Priority, PriorityOption } from '../../models/todo.model';

@Component({
  selector: 'app-todo-form',
  imports: [ReactiveFormsModule],
  templateUrl: './todo-form.component.html',
  styleUrl: './todo-form.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoFormComponent {
  priorityOptions = input.required<PriorityOption[]>();
  addTodo = output<CreateTodoInput>();

  title = signal('');
  selectedPriority = signal<Priority>('medium');

  onInputChange(event: Event) {
    const target = event.target as HTMLInputElement;

    if (!target) return;
    if (target.value.length === 0 || target.value === ' ') return;

    this.title.set(target.value);
  }

  onSelectChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    if (!target) return;

    this.selectedPriority.set(target.value as Priority);
  }

  onsubmit(): void {
    this.addTodo.emit({
      title: this.title(),
      completed: false,
      priority: this.selectedPriority(),
    });
  }
}
