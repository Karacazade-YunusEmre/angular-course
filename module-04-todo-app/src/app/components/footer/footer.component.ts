import { ChangeDetectionStrategy, Component, input, output } from '@angular/core';

@Component({
  selector: 'app-footer',
  imports: [],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class FooterComponent {
  completedCount = input.required<number>();
  clearCompletedCount = output();

  clear(): void {
    this.clearCompletedCount.emit();
  }
}
