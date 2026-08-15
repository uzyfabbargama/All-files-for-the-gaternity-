import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideServerRendering, withRoutes } from '@angular/ssr';
import { appConfig } from './app.config';
import { serverRoutes } from './app.routes.server';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(withRoutes(serverRoutes))
  ]
export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // ... otros providers que tengas
  ]
};

export const config = mergeApplicationConfig(appConfig, serverConfig);
