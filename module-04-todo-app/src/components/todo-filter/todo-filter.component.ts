import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  selector: 'app-todo-filter',
  imports: [],
  templateUrl: './todo-filter.component.html',
  styleUrl: './todo-filter.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TodoFilterComponent {}
