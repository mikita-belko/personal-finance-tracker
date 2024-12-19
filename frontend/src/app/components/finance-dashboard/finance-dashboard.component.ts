import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // Импортируем CommonModule
import { IncomeExpenseService } from '../../services/income-expense.service';

@Component({
  selector: 'app-finance-dashboard',
  standalone: true, // Standalone Component
  imports: [CommonModule], // Добавляем CommonModule
  templateUrl: './finance-dashboard.component.html',
  styleUrls: ['./finance-dashboard.component.css']
})
export class FinanceDashboardComponent implements OnInit {
  incomes: any[] = [];
  expenses: any[] = [];
  summary: any = {};

  constructor(private incomeExpenseService: IncomeExpenseService) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    // Получение доходов
    this.incomeExpenseService.getIncomes().subscribe(data => {
      this.incomes = data;
    });

    // Получение расходов
    this.incomeExpenseService.getExpenses().subscribe(data => {
      this.expenses = data;
    });

    // Получение сводной информации
    this.incomeExpenseService.getSummary().subscribe(data => {
      this.summary = data;
    });
  }

  // Удаление дохода
  deleteIncome(incomeId: number): void {
    if (confirm('Вы уверены, что хотите удалить этот доход?')) {
      this.incomeExpenseService.deleteIncome(incomeId).subscribe(() => {
        alert('Доход успешно удалён!');
        this.loadData(); // Обновляем список после удаления
      });
    }
  }
  
  // Удаление расхода
  deleteExpense(expenseId: number): void {
    if (confirm('Вы уверены, что хотите удалить этот расход?')) {
      this.incomeExpenseService.deleteExpense(expenseId).subscribe(() => {
        alert('Расход успешно удалён!');
        this.loadData(); // Обновляем список после удаления
      });
    }
  }  
}
