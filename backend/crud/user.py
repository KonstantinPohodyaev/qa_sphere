import uuid
from crud.base import CRUDBase
from models.user import User, UserRole
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    '''CRUD операции для User'''
    
    async def get_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> Optional[User]:
        '''Получить пользователя по email'''
        result = await session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()

    async def get_current_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID
    ) -> Optional[User]:
        '''Получить текущего пользователя по ID'''
        result = await session.execute(
            select(self.model).where(self.model.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(
        self,
        session: AsyncSession,
        create_schema: UserCreate,
        commit: bool = True,
    ) -> User:
        '''Создать пользователя с хешированием пароля'''
        # Получаем данные из схемы
        user_data = create_schema.model_dump(exclude={'password'})
        
        # Хешируем пароль
        user_data['password_hash'] = get_password_hash(create_schema.password)
        
        # Создаем объект пользователя
        db_user = self.model(**user_data)
        session.add(db_user)
        
        if commit:
            await session.commit()
            await session.refresh(db_user)
        
        return db_user
    
    async def update(
        self,
        session: AsyncSession,
        db_user: User,
        update_schema: UserUpdate,
        commit: bool = True,
    ) -> User:
        '''Обновить пользователя с обработкой пароля'''
        update_data = update_schema.model_dump(exclude_unset=True, exclude={'password'})
        
        # Если передан новый пароль, хешируем его
        if update_schema.password is not None:
            update_data['password_hash'] = get_password_hash(update_schema.password)
        
        # Обновляем поля
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        session.add(db_user)
        if commit:
            await session.commit()
            await session.refresh(db_user)
        
        return db_user


user_crud = CRUDUser(User)
