import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('../app/shared/layout/layout').then((m) => m.Layout),
  },
];
