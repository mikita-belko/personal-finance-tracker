import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class IncomeExpenseService {
  private apiUrl = 'http://127.0.0.1:8000'; // Базовый URL бэкенда FastAPI

  constructor(private http: HttpClient) {}

  // Получение всех доходов
  getIncomes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/incomes`);
  }

  // Получение всех расходов
  getExpenses(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/expenses`);
  }

  // Получение сводной информации
  getSummary(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/summary`);
  }
}
