'''
Главный роутер API v1
'''
from fastapi import APIRouter

from api.v1.endpoints import examples

api_router = APIRouter()

# Подключение роутеров
api_router.include_router(examples.router, prefix='/examples', tags=['examples'])
