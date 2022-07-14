import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { MatDialog } from '@angular/material/dialog';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

@Component({
  selector: 'app-schematics-navigation',
  templateUrl: './schematics-navigation.component.html',
  styleUrls: ['./schematics-navigation.component.css']
})
export class SchematicsNavigationComponent {
  faGithub = faGithub;  

  constructor(public dialog: MatDialog, private breakpointObserver: BreakpointObserver) {}

  openHelp() {
    this.dialog.open(HelpDialog);
  }

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

}

@Component({
  selector: 'help-dialog',
  templateUrl: 'help.html',
})
export class HelpDialog {}
