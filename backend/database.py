from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

# Строка подключения к PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/finance_tracker"

# Создаём асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём асинхронную сессию
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Базовый класс для моделей
Base = declarative_base()

# Генератор асинхронной сессии
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session