'''
Базовые настройки базы данных (асинхронные)
'''
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from core.config import settings

# Формирование async URL для PostgreSQL
async_database_url = settings.DATABASE_URL

# Создание асинхронного движка базы данных
async_engine = create_async_engine(
    async_database_url,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=10,  # Размер пула соединений
    max_overflow=20,  # Максимальное количество дополнительных соединений
    echo=True,  # Логирование SQL запросов (отключить в продакшене)
)

# Создание фабрики асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Базовый класс для моделей
Base = declarative_base()


async def get_async_session() -> AsyncSession:
    '''
    Dependency для получения асинхронной сессии базы данных
    '''
    async with AsyncSessionLocal() as session:
        yield session
