'''
Эндпоинты для аутентификации
'''
from datetime import timedelta
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_async_session
from schemas.user import UserLogin, Token
from crud.user import user_crud
from core.security import verify_password, create_access_token
from core.config import settings
from validators.user import (
    validate_user_email, validate_is_active, validate_password
)


router = APIRouter()


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary='Войти в систему',
    description='Получить JWT токен для аутентификации (используя JSON body)',
)
async def login_json(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Войти в систему и получить JWT токен
    '''

    user = await user_crud.get_by_email(session, login_data.email)
    
    await validate_user_email(login_data.email, session)
    await validate_is_active(user)
    await validate_password(login_data.password, user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user.id)},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type='bearer')
