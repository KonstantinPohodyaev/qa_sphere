'''
Эндпоинты для аутентификации
'''
from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_current_user
from core.config import settings
from core.security import create_access_token
from crud.user import user_crud
from database.base import get_async_session
from models.user import User
from schemas.auth import LogoutResponse
from schemas.user import Token, UserLogin
from validators.user import (validate_is_active, validate_password,
                             validate_user_email)

router = APIRouter()


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary='Войти в систему',
    description='Получить JWT токен для аутентификации. Используйте этот эндпоинт для входа через Swagger UI (форма) или JSON body.',
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Войти в систему и получить JWT токен
    
    Для Swagger UI:
    - username: email пользователя (например, admin@mail.com)
    - password: пароль пользователя
    
    Для JSON запросов используйте /login/json
    '''

    user = await user_crud.get_by_email(session, form_data.username)
    
    await validate_user_email(form_data.username, session)
    await validate_is_active(user)
    await validate_password(form_data.password, user)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user.id)},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type='bearer')


@router.post(
    '/login/json',
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary='Войти в систему (JSON)',
    description='Получить JWT токен для аутентификации используя JSON body',
)
async def login_json(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Войти в систему и получить JWT токен (используя JSON body)
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


@router.post(
    '/logout',
    status_code=status.HTTP_200_OK,
    response_model=LogoutResponse,
    summary='Выйти из системы',
    description='Выйти из системы (требуется JWT токен). Клиент должен удалить токен после этого запроса.',
)
async def logout(
    current_user: User = Depends(get_current_user)
):
    '''
    Выйти из системы
    
    Примечание: JWT токены являются stateless, поэтому сервер не может их отозвать.
    Клиент должен удалить токен после успешного выхода.
    В будущем можно реализовать blacklist токенов для более безопасного logout.
    '''
    return LogoutResponse(
        message=f'Успешный выход из системы для пользователя {current_user.email}'
    )
