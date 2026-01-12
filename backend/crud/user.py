import uuid
from typing import Optional, override

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.security import get_password_hash
from crud.base import CRUDBase
from crud.pipeline import pipeline_crud
from models.pipeline import Pipeline
from models.user import User
from schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    '''CRUD операции для User'''

    @override
    async def get_by_id(
        self,
        session: AsyncSession,
        id: uuid.UUID
    ) -> Optional[User]:
        '''Получить пользователя по ID'''
        result = await session.execute(
            select(self.model)
            .where(self.model.id == id)
            .options(selectinload(self.model.pipelines))
        )
        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        session: AsyncSession,
        email: str
    ) -> Optional[User]:
        '''Получить пользователя по email'''
        result = await session.execute(
            select(self.model)
            .where(self.model.email == email)
            .options(selectinload(self.model.pipelines))
        )
        return result.scalar_one_or_none()

    async def get_current_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID
    ) -> Optional[User]:
        '''Получить текущего пользователя по ID'''
        result = await session.execute(
            select(self.model)
            .where(self.model.id == user_id)
            .options(selectinload(self.model.pipelines))
        )
        return result.scalar_one_or_none()
    
    @override
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
            
            # Перезагружаем с связанными данными pipelines
            result = await session.execute(
                select(self.model)
                .where(self.model.id == db_user.id)
                .options(selectinload(self.model.pipelines))
            )
            db_user = result.scalar_one()
        
        return db_user

    @override
    async def update(
        self,
        session: AsyncSession,
        db_user: User,
        update_schema: UserUpdate,
        commit: bool = True,
    ) -> User:
        '''Обновить пользователя с обработкой пароля'''

        update_data = update_schema.model_dump(
            exclude_unset=True, exclude={'password', 'pipelines'}
        )
        
        if update_schema.password is not None:
            update_data['password_hash'] = get_password_hash(update_schema.password)

        for field, value in update_data.items():
            setattr(db_user, field, value)

        if update_schema.pipelines is not None:
            pipeline_ids = []
            for pipeline_data in update_schema.pipelines:
                pipeline_id = pipeline_data.get('id')
                if pipeline_id:
                    try:
                        pipeline_ids.append(uuid.UUID(str(pipeline_id)))
                    except (ValueError, TypeError):
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Некорректный pipeline_id = {pipeline_id}'
                        )
            
            if pipeline_ids:
                result = await session.execute(
                    select(Pipeline)
                    .where(Pipeline.id.in_(pipeline_ids))
                    .options(selectinload(Pipeline.owners))
                )
                pipelines = list(result.scalars().all())
                
                for pipeline in pipelines:
                    current_owner_ids = {owner.id for owner in pipeline.owners}
                    if db_user.id not in current_owner_ids:
                        pipeline.owners.append(db_user)
                        session.add(pipeline)

        if commit:
            print('commit')
            await session.flush()
            await session.commit()
            
            result = await session.execute(
                select(self.model)
                .where(self.model.id == db_user.id)
                .options(selectinload(self.model.pipelines))
            )
            db_user = result.scalar_one()
            print([p.id for p in db_user.pipelines])
        
        return db_user


user_crud = CRUDUser(User)
