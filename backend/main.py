from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# Модель доходов
class Income(BaseModel):
    id: int
    amount: float  # Сумма дохода
    source: str    # Источник дохода
    date: str      # Дата в формате 'YYYY-MM-DD'

# Модель для расходов
class Expense(BaseModel):
    id: int
    amount: float   # Сумма расхода
    category: str   # Категория расхода
    date: str       # Дата в формате 'YYYY-MM-DD'

# Временное хранилище данных
incomes: List[Income] = []
expenses: List[Expense] = []

# Создание дохода
@app.post("/incomes", status_code=201)
async def create_income(income: Income):
    # Проверка на существующий ID
    if any(i.id == income.id for i in incomes):
        raise HTTPException(status_code=400, detail="Income with this ID already exists.")
    
    incomes.append(income)
    return income

# Обновление дохода по ID
@app.put("/incomes/{income_id}")
async def update_income(income_id: int, updated_income: Income):
    for i, income in enumerate(incomes):
        if income.id == income_id:
            incomes[i] = updated_income
            return updated_income
    raise HTTPException(status_code=404, detail="Income not found")

# Получение всех доходов
@app.get("/incomes")
async def get_incomes():
    return incomes

# Получение деталей конкретного дохода
@app.get("/incomes/{income_id}")
async def get_income(income_id: int):
    for income in incomes:
        if income.id == income_id:
            return income
    raise HTTPException(status_code=404, detail="Income not found")

# Удаление дохода по ID
@app.delete("/incomes/{income_id}", status_code=204)
async def delete_income(income_id: int):
    global incomes
    # Поиск записи
    incomes = [income for income in incomes if income.id != income_id]
    return {"detail": "Income deleted successfully"}

# Создание расхода
@app.post("/expenses", status_code=201)
async def create_expense(expense: Expense):
    if any(e.id == expense.id for e in expenses):
        raise HTTPException(status_code=400, detail="Expense with this ID already exists.")
    expenses.append(expense)
    return expense

# Обновление расхода по ID
@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, updated_expense: Expense):
    for i, expense in enumerate(expenses):
        if expense.id == expense_id:
            expenses[i] = updated_expense
            return updated_expense
    raise HTTPException(status_code=404, detail="Expense not found")

# Получение всех расходов
@app.get("/expenses")
async def get_expenses():
    return expenses

# Получение деталей конкретного расхода
@app.get("/expenses/{expense_id}")
async def get_expense(expense_id: int):
    for expense in expenses:
        if expense.id == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Expense not found")

# Удаление расхода по ID
@app.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(expense_id: int):
    global expenses
    expenses = [expense for expense in expenses if expense.id != expense_id]
    return {"detail": "Expense deleted successfully"}

# Суммарные доходы и расходы
@app.get("/summary")
async def get_summary():
    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }