import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WalkComponent } from './walk.component';

describe('WalkComponent', () => {
  let component: WalkComponent;
  let fixture: ComponentFixture<WalkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WalkComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WalkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
