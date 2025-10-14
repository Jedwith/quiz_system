from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

DATABASE_URL = settings.get_db_url()

#Создание асинхронного движка для работы с бд
engine = create_async_engine(DATABASE_URL,echo=True)
# Создание фабрик сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass

async def get_db():
    async with async_session_maker() as session:
        yield session
