'''
Базовые настройки базы данных
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Создание движка базы данных
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_size=10,  # Размер пула соединений
    max_overflow=20,  # Максимальное количество дополнительных соединений
    echo=True,  # Логирование SQL запросов (отключить в продакшене)
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    '''
    Dependency для получения сессии базы данных
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
