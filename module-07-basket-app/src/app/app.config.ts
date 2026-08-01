import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { registerLocaleData } from '@angular/common';
import localeTr from '@angular/common/locales/tr';

registerLocaleData(localeTr);

import { LOCALE_ID } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    { provide: LOCALE_ID, useValue: 'tr' },
  ],
};
