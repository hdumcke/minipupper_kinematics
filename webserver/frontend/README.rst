Prerequisite
============

nvm use --lts
npm i -g @angular/cli
npm i @fortawesome/fontawesome-free
npm cache verify

Create Angular Project
======================

ng new minipupper # answer y CSS

cd minipupper
ng add @angular/material # indigo-pink , N, Y
npm i @fortawesome/angular-fontawesome
npm i @fortawesome/free-brands-svg-icons

add slider and card
-------------------

sed -i "2 aimport { MatSliderModule } from '@angular/material/slider';" src/app/app.module.ts
sed -i "2 aimport { MatCardModule } from '@angular/material/card';" src/app/app.module.ts
sed -i "2 aimport { MatButtonToggleModule } from '@angular/material/button-toggle';" src/app/app.module.ts
sed -i "2 aimport { HttpClientModule } from '@angular/common/http';" src/app/app.module.ts
sed -i "2 aimport { FontAwesomeModule } from '@fortawesome/angular-fontawesome';" src/app/app.module.ts
sed -i "2 aimport { MatDialogModule } from '@angular/material/dialog';" src/app/app.module.ts

sed -i "36 a\ \ \ \ MatSliderModule," src/app/app.module.ts
sed -i "36 a\ \ \ \ MatCardModule," src/app/app.module.ts
sed -i "36 a\ \ \ \ MatButtonToggleModule," src/app/app.module.ts
sed -i "36 a\ \ \ \ HttpClientModule," src/app/app.module.ts
sed -i "36 a\ \ \ \ FontAwesomeModule," src/app/app.module.ts
sed -i "36 a\ \ \ \ MatDialogModule," src/app/app.module.ts

add components
--------------

components="wobble walk trot gallop"
for component in $components; do
ng generate component components/$component
done

add navigation
--------------

schematics="navigation"
for schematic in $schematics; do
ng generate @angular/material:$schematic schematics/schematics-$schematic
done

sed -i "s/minipupper/Minipupper Controller/"  src//app/schematics/schematics-navigation/schematics-navigation.component.html

add links
---------

sed -i '8,10d' src/app/schematics/schematics-navigation/schematics-navigation.component.html
links=""
components="wobble walk trot gallop"
for component in $components; do
links=$links"        <a mat-list-item href=\"$component\">$component</a>\n"
done

sed -i "7 a$links" src/app/schematics/schematics-navigation/schematics-navigation.component.html

add routes
----------

OLDIFS=$IFS
components="wobble walk trot gallop"
str="const routes: Routes = ["
import=""
for component in $components; do
IFS='-'
read -a strarr <<< "$component"
IFS=$OLDIFS
caml=''
for val in "${strarr[@]}";
do
  first=`echo $val|cut -c1|tr [a-z] [A-Z]`
  second=`echo $val|cut -c2-`
  caml=$caml$first$second
done
str1="\n  { path: '$component', component: ${caml}Component },"
str=$str$str1
import=${import}"import { ${caml}Component } from './components/$component/$component.component';\n"
done

sed -i "s/const routes: Routes = \[/$str/" ./src/app/app-routing.module.ts
sed -i "2 a$import" ./src/app/app-routing.module.ts

sed  -i 's/<!-- Add Content Here -->/<router-outlet><\/router-outlet>/' src/app/schematics/schematics-navigation/schematics-navigation.component.html

update app html
---------------

echo "<app-schematics-navigation></app-schematics-navigation>" > src/app/app.component.html

add sample page
---------------

cat > src/app/components/wobble/wobble.component.html << EOF
<mat-card class="wobble-card">
  <mat-card-content>
    <h1>Wobble</h1>
    <h2>Yaw</h2>
    <mat-slider (input)="onChange('yaw', \$event.value)" min="-10" max="10" step="1" value="0" thumbLabel=True></mat-slider>
    <h2>Pitch</h2>
    <mat-slider (input)="onChange('pitch', \$event.value)" min="-10" max="10" step="1" value="0" thumbLabel=True></mat-slider>
    <h2>Roll</h2>
    <mat-slider (input)="onChange('roll', \$event.value)" min="-10" max="10" step="1" value="0" thumbLabel=True></mat-slider>
    <h2>Hight</h2>
    <mat-slider (input)="onChange('hight', \$event.value)" min="-10" max="10" step="1" value="0" thumbLabel=True></mat-slider>
    <p>
      <mat-button-toggle-group (change)="onClick(\$event.value)" name="fontStyle" aria-label="Font Style" #group="matButtonToggleGroup">
        <mat-button-toggle value="start">Start</mat-button-toggle>
        <mat-button-toggle value="stop">Stop</mat-button-toggle>
      </mat-button-toggle-group>
    </p>
  </mat-card-content>
</mat-card>
EOF

cat > src/app/components/wobble/wobble.component.ts << EOF
import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
@Component({
  selector: 'app-wobble',
  templateUrl: './wobble.component.html',
  styleUrls: ['./wobble.component.css']
})
export class WobbleComponent implements OnInit {

  private REST_API_SERVER = window.location.protocol + '//' + window.location.host + this.router.url

  loading: boolean=false;

  constructor(private http: HttpClient, private router : Router) { }

  getHttp(command: string, param: string): void {
    this.loading = true;
    this.http.get<any[]>(this.REST_API_SERVER + '/' + command + '/' + param)
             .subscribe(data => {
                 this.loading = false;
                 console.log(data);
            },
            error => {
                console.log(error);
                this.loading = false;
            }
        );

  }

  ngOnInit(): void {
  }

  onChange(slider: string, value: number | null): void{
    if(value) {
      this.getHttp(slider, value.toString())
    }
  }

  onClick(value: string): void {
    this.getHttp('status', value)
  }

}
EOF

cat > src/app/components/wobble/wobble.component.css << EOF
.mat-slider-vertical {
  height: 300px;
}

.mat-card + .mat-card {
  margin-top: 8px 16px;
}

.wobble-card h1 {
  margin: 0 8px 16px;
}

.wobble-card h2 {
  margin: 0 8px;
}
EOF

components="walk trot gallop"
for component in $components; do
first=$(echo $component|cut -c1|tr [a-z] [A-Z])
second=$(echo $component|cut -c2-)
cat > src/app/components/$component/$component.component.html << EOF
<mat-card class="$component-card">
  <mat-card-content>
    <h1>$first$second</h1>
    <mat-slider (input)="onChange('vel_x', \$event.value)" vertical min="-10" max="10" step="1" value="0" thumbLabel=True></mat-slider>
    <mat-slider (input)="onChange('vel_y', \$event.value)" min="-10" max="10" step="1" value="0" thumbLabel=True></mat-slider>
    <p>
      <mat-button-toggle-group (change)="onClick(\$event.value)" name="fontStyle" aria-label="Font Style" #group="matButtonToggleGroup">
        <mat-button-toggle value="start">Start</mat-button-toggle>
        <mat-button-toggle value="stop">Stop</mat-button-toggle>
      </mat-button-toggle-group>
    </p>
  </mat-card-content>
</mat-card>
EOF
cp src/app/components/wobble/wobble.component.css src/app/components/$component/$component.component.css
cp src/app/components/wobble/wobble.component.ts src/app/components/$component/$component.component.ts
sed -i "s/wobble/$component/" src/app/components/$component/$component.component.ts
sed -i "s/Wobble/$first$second/" src/app/components/$component/$component.component.ts
done

Test Angular Project
====================

ng serve --open

Build Angular Project
=====================

ng build
