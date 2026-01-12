import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud.pipeline_version import pipeline_version_crud
from schemas.pipeline_version import PipelineVersionRead
from api.dependencies import get_async_session
from validators.pipeline_version import validate_pipeline_version_id

router = APIRouter()

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[PipelineVersionRead],
    summary='Получить все PipelineVersion',
    description='Получить все PipelineVersion',
)
async def get_all_pipeline_versions(
    session: AsyncSession = Depends(get_async_session),
    offset: int = 0,
    limit: int = 100,
) -> list[PipelineVersionRead]:
    '''Получить все PipelineVersion'''

    return await pipeline_version_crud.get_all(session, offset, limit)

@router.get(
    '/{pipeline_version_id}',
    status_code=status.HTTP_200_OK,
    response_model=PipelineVersionRead,
    summary='Получить PipelineVersion по ID',
    description='Получить PipelineVersion по ID',
)
async def get_pipeline_version_by_id(
    pipeline_version_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
) -> PipelineVersionRead:
    '''Получить PipelineVersion по ID'''

    return await validate_pipeline_version_id(pipeline_version_id, session)
