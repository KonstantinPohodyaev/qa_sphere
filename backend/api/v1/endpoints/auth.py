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

router = APIRouter()


@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=Token,
    summary='Войти в систему',
    description='Получить JWT токен для аутентификации. В поле "username" введите email пользователя, в поле "password" - пароль.',
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Войти в систему и получить JWT токен
    
    Использует стандартную OAuth2 форму:
    - username: email пользователя (например, admin@mail.com)
    - password: пароль пользователя
    '''
    # Ищем пользователя по email (username в OAuth2 форме)
    user = await user_crud.get_by_email(session, form_data.username)
    
    # Проверяем, что пользователь существует
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверяем, что пользователь активен
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен"
        )
    
    # Проверяем пароль
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный email или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    # Создаем токен доступа
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
    description='Получить JWT токен для аутентификации (используя JSON body)',
)
async def login_json(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Войти в систему и получить JWT токен (используя JSON)
    '''
    # Ищем пользователя по email
    user = await user_crud.get_by_email(session, login_data.email)
    
    # Проверяем, что пользователь существует
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный email или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    
    # Проверяем, что пользователь активен
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен"
        )

    # Проверяем пароль
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем токен доступа
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': str(user.id)},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
