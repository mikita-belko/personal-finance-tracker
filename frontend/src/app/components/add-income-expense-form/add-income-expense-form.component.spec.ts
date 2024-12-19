import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddIncomeExpenseFormComponent } from './add-income-expense-form.component';

describe('AddIncomeExpenseFormComponent', () => {
  let component: AddIncomeExpenseFormComponent;
  let fixture: ComponentFixture<AddIncomeExpenseFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddIncomeExpenseFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddIncomeExpenseFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
