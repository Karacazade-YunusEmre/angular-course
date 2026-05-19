import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';
import { FilterMode } from '../../models/todo.model';

@Component({
  selector: 'app-todo-filter',
  imports: [],
  templateUrl: './todo-filter.component.html',
  styleUrl: './todo-filter.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoFilterComponent {
  total = input.required<number>();
  completed = input.required<number>();
  active = input.required<number>();

  activeFilter = input.required<FilterMode>();
  onChangeFilter = output<FilterMode>();

  changeFilter(filter: FilterMode): void {
    this.onChangeFilter.emit(filter);
  }
}
