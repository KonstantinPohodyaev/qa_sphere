import uuid
from typing import Optional, override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.base import CRUDBase
from models.pipeline_version import PipelineVersion
from schemas.pipeline_version import (PipelineVersionCreate,
                                      PipelineVersionUpdate)


class PipelineVersionCRUD(CRUDBase[PipelineVersion, PipelineVersionCreate, PipelineVersionUpdate]):
    '''CRUD для PipelineVersion'''

    @override
    async def get_all(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **filters
    ) -> list[PipelineVersion]:
        '''Получить все PipelineVersion с опциональными фильтрами'''

        query = (
            select(PipelineVersion)
            .options(selectinload(PipelineVersion.pipeline))
            .options(selectinload(PipelineVersion.runs))
        )
        for key, value in filters.items():
            if hasattr(PipelineVersion, key) and value is not None:
                query = query.where(getattr(PipelineVersion, key) == value)
        result = await session.execute(
            query.offset(offset).limit(limit)
        )
        return list(result.scalars().all())
    
    @override
    async def get_by_id(
        self,
        session: AsyncSession,
        id: uuid.UUID
    ) -> Optional[PipelineVersion]:
        '''Получить PipelineVersion по ID'''
        return (
            await session.execute(
                select(PipelineVersion)
                .where(PipelineVersion.id == id)
                .options(selectinload(PipelineVersion.pipeline))
                .options(selectinload(PipelineVersion.runs))
            )
        ).scalar_one_or_none()


pipeline_version_crud = PipelineVersionCRUD(PipelineVersion)
