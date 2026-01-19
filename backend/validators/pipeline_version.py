import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.pipeline_version import pipeline_version_crud
from models.pipeline_version import PipelineVersion


async def validate_pipeline_version_id(
    pipeline_version_id: uuid.UUID,
    session: AsyncSession
) -> PipelineVersion:
    '''Валидация ID PipelineVersion'''
    pipeline_version = await pipeline_version_crud.get_by_id(
        session, pipeline_version_id
    )
    if not pipeline_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'PipelineVersion с ID = {pipeline_version_id} не найден'
        )
    return pipeline_version
