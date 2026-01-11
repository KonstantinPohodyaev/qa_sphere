'''
CRUD операции для Pipeline
'''
import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from models.pipeline import Pipeline
from schemas.pipeline import PipelineCreate, PipelineUpdate


class CRUDPipeline(CRUDBase[Pipeline, PipelineCreate, PipelineUpdate]):
    '''CRUD операции для Pipeline с учетом user_id'''

    async def get_all_pipelines(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100
    ) -> list[Pipeline]:
        '''Получить все пайплайны'''
        return (
            await session.execute(
                select(Pipeline)
                .offset(offset)
                .limit(limit)
                .options(selectinload(Pipeline.user))
            )
        ).scalars().all()
    
    async def get_by_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100
    ) -> list[Pipeline]:
        '''Получить все пайплайны пользователя'''
        return await self.get_all(session, offset=offset, limit=limit, user_id=user_id)

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
        '''Создать пайплайн для пользователя'''
        # Убеждаемся, что user_id в схеме соответствует переданному
        schema_data = create_schema.model_dump()
        schema_data['user_id'] = user_id
        
        db_object = Pipeline(**schema_data)
        session.add(db_object)
        if commit:
            await session.commit()
            await session.refresh(db_object)
        return db_object
    
    async def update_for_user(
        self,
        session: AsyncSession,
        pipeline_id: uuid.UUID,
        user_id: uuid.UUID,
        update_schema: PipelineUpdate,
        commit: bool = True
    ) -> Optional[Pipeline]:
        '''Обновить пайплайн с проверкой владельца'''
        db_object = await self.get_by_id_with_user(session, pipeline_id, user_id)
        if not db_object:
            return None
        
        return await self.update(session, db_object, update_schema, commit=commit)
    
    async def delete_for_user(
        self,
        session: AsyncSession,
        pipeline_id: uuid.UUID,
        user_id: uuid.UUID,
        commit: bool = True
    ) -> bool:
        '''Удалить пайплайн с проверкой владельца'''
        db_object = await self.get_by_id_with_user(session, pipeline_id, user_id)
        if not db_object:
            return False
        
        await self.delete(session, db_object, commit=commit)
        return True


pipeline_crud = CRUDPipeline(Pipeline)
