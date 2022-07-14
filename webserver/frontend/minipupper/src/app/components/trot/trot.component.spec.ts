import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrotComponent } from './trot.component';

describe('TrotComponent', () => {
  let component: TrotComponent;
  let fixture: ComponentFixture<TrotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TrotComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
