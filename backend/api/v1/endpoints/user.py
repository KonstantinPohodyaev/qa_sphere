import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.dependencies import get_current_user as get_current_user_dependency
from crud.user import user_crud
from database.base import get_async_session
from models.user import User
from schemas.user import UserCreate, UserRead, UserUpdate
from validators.user import validate_user_email, validate_user_id

router = APIRouter()


@router.get(
    '/my-user',
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    summary='Получить текущего пользователя',
    description='Получить текущего пользователя (требуется JWT токен в заголовке Authorization: Bearer <token>)',
)
async def get_current_user(
    current_user: User = Depends(get_current_user_dependency),
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить текущего пользователя'''

    return await user_crud.get_current_user(session, current_user.id)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[UserRead],
    summary='Получить всех пользователей',
    description='Получить всех пользователей',
)
async def get_all_users(
    current_user: User = Depends(get_current_user_dependency),
    session: AsyncSession = Depends(get_async_session),
):
    '''Получить всех пользователей'''

    return await user_crud.get_all(session)


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    summary='Получить пользователя по ID',
    description='Получить пользователя по ID',
)
async def get_user_by_id(
    user_id: uuid.UUID,
    current_user: User = Depends(get_current_user_dependency),
    session: AsyncSession = Depends(get_async_session),
):
    '''Получить пользователя по ID'''

    return await validate_user_id(user_id, session)


@router.get(
    '/email/{email}',
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    summary='Получить пользователя по email',
    description='Получить пользователя по email',
)
async def get_user_by_email(
    email: str,
    current_user: User = Depends(get_current_user_dependency),
    session: AsyncSession = Depends(get_async_session),
):
    '''Получить пользователя по email'''

    return await validate_user_email(email, session)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserRead,
    summary='Создать пользователя',
    description='Создать пользователя',
)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Создать пользователя'''
    return await user_crud.create(session, user)


@router.patch(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserRead,
    summary='Обновить пользователя',
    description='Обновить пользователя',
)
async def update_user(
    user_id: uuid.UUID,
    user: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Обновить пользователя'''

    db_user = await validate_user_id(user_id, session)
    return await user_crud.update(session, db_user, user)


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    summary='Удалить пользователя',
    description='Удалить пользователя',
)
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
):
    '''Удалить пользователя'''
    return await user_crud.delete(session, user_id)
