import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GallopComponent } from './gallop.component';

describe('GallopComponent', () => {
  let component: GallopComponent;
  let fixture: ComponentFixture<GallopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GallopComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GallopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
