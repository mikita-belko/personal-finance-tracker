import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IncomeExpenseService } from '../../services/income-expense.service';

@Component({
  selector: 'app-add-income-expense-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './add-income-expense-form.component.html',
  styleUrls: ['./add-income-expense-form.component.css']
})
export class AddIncomeExpenseFormComponent {
  @Output() recordAdded = new EventEmitter<void>(); // Создаём событие

  recordType: string = 'income';
  amount: number = 0;
  description: string = '';
  date: string = '';

  constructor(private incomeExpenseService: IncomeExpenseService) {}

  onSubmit(): void {
    const payload = {
      amount: this.amount,
      source: this.description,
      category: this.description,
      date: this.date,
    };

    if (this.recordType === 'income') {
      this.incomeExpenseService.createIncome(payload).subscribe(() => {
        alert('Доход успешно добавлен!');
        this.recordAdded.emit(); // Сообщаем о добавлении записи
      });
    } else {
      this.incomeExpenseService.createExpense(payload).subscribe(() => {
        alert('Расход успешно добавлен!');
        this.recordAdded.emit(); // Сообщаем о добавлении записи
      });
    }
  }
}
