import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WobbleComponent } from './wobble.component';

describe('WobbleComponent', () => {
  let component: WobbleComponent;
  let fixture: ComponentFixture<WobbleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WobbleComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WobbleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
