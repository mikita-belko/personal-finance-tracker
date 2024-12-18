import datetime
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi import Depends
from database import engine, Base
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Income as IncomeModel, Expense as ExpenseModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Действие при запуске приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized")  # Лог при успешном старте

    yield  # Переходим к обработке запросов

    # Действие при завершении работы приложения
    print("Application shutdown")  # Лог при завершении работы

app = FastAPI(lifespan=lifespan)

# Pydantic-схема для доходов
class Income(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма дохода должна быть положительной")          # Сумма дохода
    source: str = Field(..., min_length=3, description="Источник дохода не может быть пустым")      # Источник дохода
    date: datetime.date = Field(..., description="Дата должна быть в формате YYYY-MM-DD")                    # Дата в формате 'YYYY-MM-DD'

# Pydantic-схема для расходов
class Expense(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма расхода должна быть положительной")         # Сумма расхода
    category: str = Field(..., min_length=3, description="Категория расхода не может быть пустой")  # Категория расхода
    date: datetime.date = Field(..., description="Дата должна быть в формате YYYY-MM-DD")                    # Дата в формате 'YYYY-MM-DD'

# --- ДОХОДЫ ---

# Создание дохода
@app.post("/incomes", status_code=201)
async def create_income(income: Income, session: AsyncSession = Depends(get_session)):
    db_income = IncomeModel(**income.model_dump())
    session.add(db_income)
    await session.commit()
    await session.refresh(db_income)
    return db_income

# Получение всех доходов
@app.get("/incomes")
async def get_incomes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(IncomeModel))
    incomes = result.scalars().all()
    return incomes

# Получение деталей конкретного дохода
@app.get("/incomes/{income_id}")
async def get_income(income_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(IncomeModel).where(IncomeModel.id == income_id))
    income = result.scalars().first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    return income

# Обновление дохода по ID
@app.put("/incomes/{income_id}")
async def update_income(income_id: int, updated_income: Income, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(IncomeModel).where(IncomeModel.id == income_id))
    income = result.scalars().first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    income.amount = updated_income.amount
    income.source = updated_income.source
    income.date = updated_income.date
    await session.commit()
    return income

# Удаление дохода по ID
@app.delete("/incomes/{income_id}", status_code=204)
async def delete_income(income_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(IncomeModel).where(IncomeModel.id == income_id))
    income = result.scalars().first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    await session.delete(income)
    await session.commit()
    return {"detail": "Income deleted successfully"}

# --- РАСХОДЫ ---

# Создание расхода
@app.post("/expenses", status_code=201)
async def create_expense(expense: Expense, session: AsyncSession = Depends(get_session)):
    db_expense = ExpenseModel(**expense.model_dump())
    session.add(db_expense)
    await session.commit()
    await session.refresh(db_expense)
    return db_expense

# Получение всех расходов
@app.get("/expenses")
async def get_expenses(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ExpenseModel))
    expenses = result.scalars().all()
    return expenses

# Получение деталей конкретного расхода
@app.get("/expenses/{expense_id}")
async def get_expense(expense_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ExpenseModel).where(ExpenseModel.id == expense_id))
    expense = result.scalars().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

# Обновление расхода по ID
@app.put("/expenses/{expense_id}")
async def update_expense(expense_id: int, updated_expense: Expense, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ExpenseModel).where(ExpenseModel.id == expense_id))
    expense = result.scalars().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense.amount = updated_expense.amount
    expense.category = updated_expense.category
    expense.date = updated_expense.date
    await session.commit()
    return expense

# Удаление расхода по ID
@app.delete("/expenses/{expense_id}", status_code=204)
async def delete_expense(expense_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ExpenseModel).where(ExpenseModel.id == expense_id))
    expense = result.scalars().first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    await session.delete(expense)
    await session.commit()
    return {"detail": "Expense deleted successfully"}

# --- СУММАРНЫЕ ДОХОДЫ И РАСХОДЫ ---

@app.get("/summary")
async def get_summary(session: AsyncSession = Depends(get_session)):
    result_incomes = await session.execute(select(IncomeModel))
    result_expenses = await session.execute(select(ExpenseModel))
    total_income = sum(income.amount for income in result_incomes.scalars().all())
    total_expense = sum(expense.amount for expense in result_expenses.scalars().all())
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }