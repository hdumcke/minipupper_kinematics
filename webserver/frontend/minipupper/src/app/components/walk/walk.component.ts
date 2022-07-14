import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

type Ret = {
  [key: string]: any;
};

@Injectable({
  providedIn: 'root'
})
@Component({
  selector: 'app-walk',
  templateUrl: './walk.component.html',
  styleUrls: ['./walk.component.css']
})
export class WalkComponent implements OnInit {

  velx: number | null = 0;
  vely: number | null = 0;
  freq: number | null = 120;
  stepl: number | null = 4;
  steph: number | null = 1;
  nump: number | null = 10;

  private REST_API_SERVER = window.location.protocol + '//' + window.location.host + this.router.url

  loading: boolean=false;

  constructor(private http: HttpClient, private router : Router) { }

  getHttp(command: string, param: string): void {
    this.loading = true;
    this.http.get<Ret>(this.REST_API_SERVER + '/' + command + '/' + param)
             .subscribe(data => {
                 this.loading = false;
                 console.log(data);
		this.velx = data['vel_x']
		this.vely = data['vel_y']
		this.freq = data['frequency']
		this.stepl = data['step_length']
		this.steph = data['step_height']
		this.nump = data['number_of_points']
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
