'''
Создание начальных данных при запуске приложения
'''
import contextlib
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.config import settings
from database.base import get_async_session
from crud.user import user_crud
from schemas.user import UserCreate
from models.user import UserRole


get_async_session_context = contextlib.asynccontextmanager(get_async_session)


class UserAlreadyExists(Exception):
    '''Пользователь уже существует'''
    pass


async def create_user(
    email: EmailStr,
    password: str,
    is_superuser: bool = False,
    session: AsyncSession | None = None
):
    '''
    Создать пользователя
    
    Args:
        email: Email пользователя
        password: Пароль пользователя
        is_superuser: Создать как суперпользователя (admin)
        session: Опциональная сессия БД (если не указана, создается новая)
    '''
    if session:
        # Используем переданную сессию
        existing_user = await user_crud.get_by_email(session, email)
        if existing_user:
            raise UserAlreadyExists(f'Пользователь с  email {email} уже есть')
        
        role = UserRole.ADMIN if is_superuser else UserRole.USER
        try:
            user = await user_crud.create(
                session,
                UserCreate(
                    email=email,
                    password=password,
                    role=role,
                    is_active=True
                ),
                commit=True
            )
            return user
        except IntegrityError:
            # Обработка race condition - пользователь мог быть создан между проверкой и созданием
            raise UserAlreadyExists(f'Пользователь с  email {email} уже есть')
    else:
        # Создаем новую сессию
        async with get_async_session_context() as session:
            existing_user = await user_crud.get_by_email(session, email)
            if existing_user:
                raise UserAlreadyExists(f'Пользователь с  email {email} уже есть')
            
            role = UserRole.ADMIN if is_superuser else UserRole.USER
            try:
                user = await user_crud.create(
                    session,
                    UserCreate(
                        email=email,
                        password=password,
                        role=role,
                        is_active=True
                    ),
                    commit=True
                )
                return user
            except IntegrityError:
                # Обработка race condition
                raise UserAlreadyExists(f'Пользователь с  email {email} уже есть')


async def create_first_superuser():
    '''
    Создать первого суперпользователя при запуске приложения
    '''
    if (
        settings.FIRST_SUPERUSER_EMAIL is not None
        and settings.FIRST_SUPERUSER_PASSWORD is not None
    ):
        try:
            await create_user(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True
            )
        except UserAlreadyExists:
            pass  # Пользователь уже существует, пропускаем
