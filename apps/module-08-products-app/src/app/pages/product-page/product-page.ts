import { Component } from '@angular/core';
import { ProductForm } from './components/product-form/product-form';
import { ProductFilter } from './components/product-filter/product-filter';
import { ProductTable } from './components/product-table/product-table';

@Component({
  imports: [ProductForm, ProductFilter, ProductTable],
  selector: 'app-product-page',
  styleUrl: './product-page.scss',
  templateUrl: './product-page.html',
})
export class ProductPage {}
