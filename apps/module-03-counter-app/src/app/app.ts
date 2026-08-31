import { Component, computed, signal } from '@angular/core';

interface HistoryEntry {
  oldValue: number;
  newValue: number;
  delta: number;
  timestamp: Date;
}

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly count = signal(0);
  protected readonly step = signal(1);
  protected readonly history = signal<HistoryEntry[]>([]);

  protected readonly isPositive = computed(() => this.count() > 0);
  protected readonly isNegative = computed(() => this.count() < 0);
  protected readonly isZero = computed(() => this.count() === 0);
  protected readonly isEven = computed(() => this.count() % 2 === 0);

  protected readonly maxValue = computed(() => {
    const all = [this.count(), ...this.history().map((entry) => entry.newValue)];
    return Math.max(...all);
  });
  protected readonly minValue = computed(() => {
    const all = [this.count(), ...this.history().map((entry) => entry.newValue)];
    return Math.min(...all);
  });

  protected increment(): void {
    this.changeBy(this.step());
  }

  protected decrement(): void {
    this.changeBy(-this.step());
  }

  protected reset(): void {
    this.changeBy(-this.count());
  }

  protected setStep(newStep: number): void {
    this.step.set(newStep);
  }

  private changeBy(delta: number): void {
    if (delta === 0) return;

    const oldValue = this.count();
    const newValue = oldValue + delta;

    this.count.set(newValue);

    // History'e ekle (max 5 entry)
    this.history.update((h) =>
      [{ oldValue, newValue, delta, timestamp: new Date() }, ...h].slice(0, 5),
    );
  }
}
