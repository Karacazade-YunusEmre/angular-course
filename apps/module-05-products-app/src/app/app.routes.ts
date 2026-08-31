import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./components/product-list/product-list').then((m) => m.ProductList),
    pathMatch: 'full',
  },
  {
    path: 'product/:id',
    loadComponent: () =>
      import('./components/product-detail/product-detail').then((m) => m.ProductDetail),
  },
];
