'''
Главный роутер API v1
'''
from fastapi import APIRouter

from api.v1.endpoints import pipelines

api_router = APIRouter()

# Подключение роутеров
api_router.include_router(pipelines.router, prefix='/pipelines', tags=['pipelines'])