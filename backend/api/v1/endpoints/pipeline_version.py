import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_async_session
from crud.pipeline_version import pipeline_version_crud
from schemas.pipeline_version import (PipelineVersionCreate,
                                      PipelineVersionRead,
                                      PipelineVersionUpdate)
from validators.pipeline import validate_pipeline_id
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


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=PipelineVersionRead,
    summary='Создать новую версию пайплайна',
    description='Создает версию пайплайна',
)
async def create_pipeline_version(
    create_schema: PipelineVersionCreate,
    session: AsyncSession = Depends(get_async_session)
):
    '''Создать новую версию пайплайна'''

    await validate_pipeline_id(create_schema.pipeline_id, session)
    new_pipeline_version = await pipeline_version_crud.create(session, create_schema)
    return await pipeline_version_crud.get_by_id(session, new_pipeline_version.id)


@router.patch(
    '/{pipeline_version_id}',
    status_code=status.HTTP_200_OK,
    response_model=PipelineVersionRead,
    summary='Обновление версии пайплайна',
    description='Обновление версии пайплайна'
)
async def update_pipeline_version(
    update_schema: PipelineVersionUpdate,
    pipeline_version_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
):
    '''Обновление версии пайплайна'''

    current_pipeline_version = await validate_pipeline_version_id(pipeline_version_id, session)
    pipeline_version_id = current_pipeline_version.id
    await pipeline_version_crud.update(
        session,
        current_pipeline_version,
        update_schema,
    )
    return await pipeline_version_crud.get_by_id(
        session, pipeline_version_id
    )


@router.delete(
    '/{pipeline_version_id}',
    summary='Удаление версии пайплайна',
    description='Удаление версии пайплайна'
)
async def delete_pipeline_version(
    pipeline_version_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    '''Удаление версии пайплайна'''

    db_pipeline_version = await validate_pipeline_version_id(
        pipeline_version_id, session
    )
    return await pipeline_version_crud.delete(session, db_pipeline_version)


@router.get(
    '/{pipeline_version_id}/active',
    status_code=status.HTTP_200_OK,
    response_model=PipelineVersionRead,
    summary='Получить активную версию пайплайна',
    description='Получить активную версию пайплайна'
)
async def get_active_pipeline_version(
    pipeline_version_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить активную версию пайплайна'''

    await validate_pipeline_version_id(pipeline_version_id, session)
    return await pipeline_version_crud.get_active_by_pipeline_id(
        session,
        pipeline_version_id
    )
