import { ChangeDetectionStrategy, Component, input } from '@angular/core';

@Component({
  selector: 'app-todo-stats',
  imports: [],
  templateUrl: './todo-stats.component.html',
  styleUrl: './todo-stats.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoStatsComponent {
  total = input.required<number>();
  completed = input.required<number>();
  active = input.required<number>();

  high = input.required<number>();
  medium = input.required<number>();
  low = input.required<number>();
}
