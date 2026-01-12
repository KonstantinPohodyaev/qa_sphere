'''
Главный файл приложения FastAPI
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import api_router
from core.config import settings
from core.initial_data import create_first_superuser
from database.base import Base, async_engine
# Импорт всех моделей для создания таблиц
from models import Pipeline, PipelineRun, PipelineVersion, User  # noqa: F401

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Подключение роутеров
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event('startup')
async def startup_event():
    '''Создание таблиц и начальных данных при запуске приложения'''
    # Создание таблиц
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Создание первого суперпользователя
    await create_first_superuser()


@app.on_event('shutdown')
async def shutdown_event():
    '''Закрытие соединений при остановке приложения'''
    await async_engine.dispose()


@app.get('/')
async def root():
    '''Корневой эндпоинт'''
    return {'message': 'Welcome to FastAPI application'}


@app.get('/health')
async def health_check():
    '''Проверка здоровья приложения'''
    return {'status': 'healthy'}
