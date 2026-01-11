from fastapi import APIRouter, status, Depends
from models.user import User

from schemas.user import UserRead
from api.dependencies import get_current_user as get_current_user_dependency

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    summary='Получить текущего пользователя',
    description='Получить текущего пользователя (требуется JWT токен в заголовке Authorization: Bearer <token>)',
)
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency)
):
    '''Получить текущего пользователя'''
    return current_user
