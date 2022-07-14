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
  selector: 'app-wobble',
  templateUrl: './wobble.component.html',
  styleUrls: ['./wobble.component.css']
})
export class WobbleComponent implements OnInit {

  roll: number | null = 0;
  pitch: number | null = 0;
  yaw: number | null = 0;
  height: number | null = 0;

  private REST_API_SERVER = window.location.protocol + '//' + window.location.host + this.router.url
  
  loading: boolean=false;

  constructor(private http: HttpClient, private router : Router) { }

  getHttp(command: string, param: string): void {
    this.loading = true;
    this.http.get<Ret>(this.REST_API_SERVER + '/' + command + '/' + param)
             .subscribe(data => {
                 this.loading = false;
                 console.log(data);
		 this.roll = data['roll']
		 this.pitch = data['pitch']
		 this.yaw = data['yaw']
		 this.height = data['height']
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
