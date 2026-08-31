import { Component } from '@angular/core';
import { ProductPage } from '@app/pages/product-page/product-page';

@Component({
  imports: [ProductPage],
  selector: 'app-layout',
  styleUrl: './layout.scss',
  templateUrl: './layout.html',
})
export class Layout {}
