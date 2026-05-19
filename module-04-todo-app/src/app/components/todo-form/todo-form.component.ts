import { ChangeDetectionStrategy, Component, computed, input, output, signal } from '@angular/core';
import { CreateTodoInput, Priority, PriorityOption } from '../../models/todo.model';

@Component({
  selector: 'app-todo-form',
  imports: [],
  templateUrl: './todo-form.component.html',
  styleUrl: './todo-form.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoFormComponent {
  priorityOptions = input.required<PriorityOption[]>();
  addTodo = output<CreateTodoInput>();

  title = signal('');
  selectedPriority = signal<Priority>('medium');

  isValid = computed(() => this.title().trim().length > 0);

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

  onSubmit(evet: Event): void {
    evet.preventDefault();
    if (this.title().trim().length === 0) return;

    this.addTodo.emit({
      title: this.title(),
      completed: false,
      priority: this.selectedPriority(),
    });

    this.title.set('');
    this.selectedPriority.set('medium');
  }
}
