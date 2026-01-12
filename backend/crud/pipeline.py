'''
CRUD операции для Pipeline
'''
import uuid
from typing import Optional, override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from models.pipeline import Pipeline
from models.user import User
from schemas.pipeline import PipelineCreate, PipelineUpdate


class CRUDPipeline(CRUDBase[Pipeline, PipelineCreate, PipelineUpdate]):
    '''CRUD операции для Pipeline'''

    async def get_all_pipelines(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        is_active: bool = True,
        order_by: str = 'created_at',
    ) -> list[Pipeline]:
        '''Получить все пайплайны'''
        return (
            await session.execute(
                select(Pipeline)
                .where(Pipeline.is_active == is_active)
                .offset(offset)
                .limit(limit)
                .options(selectinload(Pipeline.owners))
            )
        ).scalars().all()

    @override
    async def get_by_id(
        self,
        session: AsyncSession,
        id: uuid.UUID
    ) -> Optional[Pipeline]:
        '''Получить пайплайн по ID'''
        return (
            await session.execute(
                select(Pipeline)
                .where(Pipeline.id == id)
                .options(selectinload(Pipeline.owners))
            )
        ).scalar_one_or_none()

    async def get_by_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100
    ) -> list[Pipeline]:
        '''Получить все пайплайны пользователя (где пользователь является владельцем)'''
        from models.pipeline import pipeline_owners
        return (
            await session.execute(
                select(Pipeline)
                .join(pipeline_owners, Pipeline.id == pipeline_owners.c.pipeline_id)
                .where(pipeline_owners.c.user_id == user_id)
                .offset(offset)
                .limit(limit)
                .options(selectinload(Pipeline.owners))
            )
        ).scalars().all()

    async def get_by_code(
        self,
        session: AsyncSession,
        code: str
    ) -> Optional[Pipeline]:
        '''Получить пайплайн по коду'''
        return (
            await session.execute(
                select(Pipeline)
                .where(Pipeline.code == code)
            )
        ).scalar_one_or_none()

    async def get_by_name(
        self,
        session: AsyncSession,
        name: str
    ) -> Optional[Pipeline]:
        '''Получить пайплайн по названию'''
        return (
            await session.execute(
                select(Pipeline)
                .where(Pipeline.name == name)
            )
        ).scalar_one_or_none()

    
    async def create_for_user(
        self,
        session: AsyncSession,
        create_schema: PipelineCreate,
        user_id: uuid.UUID,
        commit: bool = True
    ) -> Pipeline:
        '''Создать пайплайн для пользователя и добавить пользователя как владельца'''
        schema_data = create_schema.model_dump()
        
        db_object = Pipeline(**schema_data)
        
        user = await session.get(User, user_id)
        if user:
            db_object.owners.append(user)
        
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object, ['owners'])
        return db_object

    async def update(
        self,
        session: AsyncSession,
        db_object: Pipeline,
        update_schema: PipelineUpdate,
        commit: bool = True
    ) -> Pipeline:
        '''Обновить пайплайн с обработкой owners'''

        update_data = update_schema.model_dump(exclude_unset=True, exclude={'owners'})
        
        for field, value in update_data.items():
            setattr(db_object, field, value)
        
        if update_schema.owners is not None:
            await session.refresh(db_object, ['owners'])
            current_owner_ids = {owner.id for owner in db_object.owners}

            owner_ids = []
            for owner_data in update_schema.owners:
                owner_id = owner_data.get('id')
                if owner_id:
                    try:
                        owner_ids.append(uuid.UUID(str(owner_id)))
                    except (ValueError, TypeError):
                        continue

            if owner_ids:
                result = await session.execute(
                    select(User).where(User.id.in_(owner_ids))
                )
                users = list(result.scalars().all())

                for user in users:
                    if user.id not in current_owner_ids:
                        db_object.owners.append(user)

        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object, ['owners'])
        
        return db_object


pipeline_crud = CRUDPipeline(Pipeline)
