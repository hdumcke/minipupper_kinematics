import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WobbleComponent } from './components/wobble/wobble.component';
import { WalkComponent } from './components/walk/walk.component';
import { TrotComponent } from './components/trot/trot.component';
import { GallopComponent } from './components/gallop/gallop.component';


const routes: Routes = [
  { path: '', redirectTo: '/wobble', pathMatch: 'full' },
  { path: 'wobble', component: WobbleComponent },
  { path: 'walk', component: WalkComponent },
  { path: 'trot', component: TrotComponent },
  { path: 'gallop', component: GallopComponent },];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
