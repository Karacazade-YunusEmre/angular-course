import { Component, output, signal } from '@angular/core';

@Component({
  selector: 'app-task-input',
  imports: [],
  templateUrl: './task-input.html',
  styleUrl: './task-input.scss',
})
export class TaskInput {
  readonly taskAdded = output<string>();

  protected readonly title = signal('');

  protected add(): void {
    const value = this.title().trim();
    if (!value) return;
    this.taskAdded.emit(value);
    this.title.set('');
  }

  protected onInput(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.title.set(target.value);
  }
}
