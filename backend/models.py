from sqlalchemy import Column, Integer, Float, String
from sqlalchemy import Date
from database import Base

# Модель доходов
class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    date = Column(Date, nullable=False)

# Модель расходов
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)