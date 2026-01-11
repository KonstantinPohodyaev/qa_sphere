'''
Главный роутер API v1
'''
from fastapi import APIRouter

from api.v1.endpoints import pipelines
from api.v1.endpoints import user
from api.v1.endpoints import auth


api_router = APIRouter()

# Подключение роутеров
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(pipelines.router, prefix='/pipelines', tags=['pipelines'])
api_router.include_router(user.router, prefix='/user', tags=['user'])
