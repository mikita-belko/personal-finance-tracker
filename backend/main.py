from pydantic import BaseModel
from typing import List

# Модель для создания дохода
class Income(BaseModel):
    id: int
    amount: float  # Сумма дохода
    source: str    # Источник дохода
    date: str      # Дата в формате 'YYYY-MM-DD'

# Хранилище доходов (временное)
incomes: List[Income] = []

from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

# Создание дохода
@app.post("/income", status_code=201)
async def create_income(income: Income):
    # Проверка на существующий ID
    if any(i.id == income.id for i in incomes):
        raise HTTPException(status_code=400, detail="Income with this ID already exists.")
    
    incomes.append(income)
    return income

# Получение всех доходов
@app.get("/income")
async def get_incomes():
    return incomes