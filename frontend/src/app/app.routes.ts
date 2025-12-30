import { Routes } from '@angular/router';
import { IntakeFormComponent } from './pages/intake-form/intake-form.component';
import { RequestsListComponent } from './pages/requests-list/requests-list.component';

export const routes: Routes = [
  { path: '', redirectTo: '/requests', pathMatch: 'full' },
  { path: 'intake', component: IntakeFormComponent },
  { path: 'requests', component: RequestsListComponent },
  { path: '**', redirectTo: '/requests' }
];
