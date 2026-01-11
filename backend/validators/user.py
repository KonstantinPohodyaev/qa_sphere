'''
Валидаторы для User
'''
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from database.base import get_async_session
from crud.user import user_crud
from models.user import User
from core.security import verify_password


async def validate_user_id(
    user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    '''Валидация ID пользователя'''
    user = await user_crud.get_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователя в UUID = {user_id} не существует'
        )


async def validate_user_email(
    email: str, session: AsyncSession
):
    '''Валидация email пользователя'''
    user = await user_crud.get_by_email(session, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователя с email = {email} не существует'
        )


async def validate_is_active(
    user: User
):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Пользователь неактивен: is_active = {user.is_active}'
        )

async def validate_password(
    password: str, user: User
):
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный пароль'
        )
