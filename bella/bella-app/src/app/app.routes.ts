import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { AboutComponent } from './components/about/about.component';
import { BellaComponent } from './components/bella/bella.component';

export const routes: Routes = [
  { path: '', component: HomeComponent, pathMatch: 'full' },
  { path: 'about', component: AboutComponent },
  { path: 'bella', component: BellaComponent },
  { path: '**', redirectTo: '' }
];
