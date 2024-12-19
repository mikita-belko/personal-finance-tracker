import { Component, ViewChild } from '@angular/core';
import { AddIncomeExpenseFormComponent } from './components/add-income-expense-form/add-income-expense-form.component';
import { FinanceDashboardComponent } from './components/finance-dashboard/finance-dashboard.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AddIncomeExpenseFormComponent, FinanceDashboardComponent], // Добавляем компоненты
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  @ViewChild(FinanceDashboardComponent) dashboard!: FinanceDashboardComponent;

  onRecordAdded(): void {
    this.dashboard.loadData(); // Вызываем обновление данных
  }
}

