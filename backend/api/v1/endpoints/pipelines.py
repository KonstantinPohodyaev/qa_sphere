'''
Эндпоинты для работы с Pipeline
'''
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from crud.pipeline import pipeline_crud
from crud.pipeline_version import pipeline_version_crud
from database.base import get_async_session
from models.pipeline import Pipeline
from schemas.pipeline import PipelineCreate, PipelineRead, PipelineUpdate
from schemas.pipeline_version import PipelineVersionRead
from validators.pipeline import (validate_pipeline_code, validate_pipeline_id,
                                 validate_pipeline_name)
from validators.user import validate_user_id

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[PipelineRead],
    summary='Получить список всех пайплайнов',
    description='Получить список всех пайплайнов',
)
async def get_all_pipelines(
    offset: int = 0,
    limit: int = 100,
    is_active: bool = True,
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить список всех пайплайнов'''
    return await pipeline_crud.get_all_pipelines(session, offset, limit, is_active)


@router.get(
    '/user',
    status_code=status.HTTP_200_OK,
    response_model=List[PipelineRead],
    summary='Получить список пайплайнов текущего пользователя',
    description='Получить список пайплайнов текущего пользователя',
)
async def get_users_pipelines(
    user_id: uuid.UUID,  # TODO: Получать из токена/сессии
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить список пайплайнов пользователя'''
    pipelines_list = await pipeline_crud.get_by_user(
        session,
        user_id=user_id,
        offset=offset,
        limit=limit
    )
    
    return pipelines_list


@router.get(
    '/{pipeline_id}',
    status_code=status.HTTP_200_OK,
    response_model=PipelineRead,
    summary='Получить пайплайн по ID',
    description='Получить пайплайн по ID',
)
async def get_pipeline(
    pipeline_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить пайплайн по ID'''
    db_pipeline = await pipeline_crud.get_by_id(
        session,
        pipeline_id
    )
    if not db_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pipeline not found or access denied'
        )
    return (
        await session.execute(
            select(Pipeline)
            .where(Pipeline.id == pipeline_id)
            .options(selectinload(Pipeline.owners))
        )
    ).scalar_one_or_none()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=PipelineRead,
    summary='Создать пайплайн',
    description='Создать новый пайплайн для текущего пользователя',
)
async def create_pipeline(
    pipeline_data: PipelineCreate,
    user_id: uuid.UUID,  # TODO: Получать из токена/сессии
    session: AsyncSession = Depends(get_async_session)
):
    '''Создать новый пайплайн'''

    # Вызов валидоторов
    await validate_user_id(user_id, session)
    await validate_pipeline_code(pipeline_data.code, session)
    await validate_pipeline_name(pipeline_data.name, session)

    db_pipeline = await pipeline_crud.create_for_user(
        session,
        create_schema=pipeline_data,
        user_id=user_id
    )
    return (
        await session.execute(
            select(Pipeline)
            .where(Pipeline.id == db_pipeline.id)
            .options(selectinload(Pipeline.owners))
        )
    ).scalar_one_or_none()


@router.patch(
    '/{pipeline_id}',
    status_code=status.HTTP_200_OK,
    response_model=PipelineRead,
    summary='Частично обновить пайплайн',
    description='Частично обновить пайплайн по ID (можно передать только изменяемые поля)',
)
async def update_pipeline(
    pipeline_id: uuid.UUID,
    pipeline_data: PipelineUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    '''Частично обновить пайплайн'''

    db_pipeline = await validate_pipeline_id(pipeline_id, session)
    await validate_pipeline_code(pipeline_data.code, session)
    await validate_pipeline_name(pipeline_data.name, session)
    
    db_pipeline = await pipeline_crud.update(
        session,
        db_pipeline,
        pipeline_data,
        commit=True
    )
    return await pipeline_crud.get_by_id(session, pipeline_id)


@router.delete(
    '/{pipeline_id}',
    status_code=status.HTTP_200_OK,
    summary='Удалить пайплайн',
    description='Удалить пайплайн по ID',
)
async def delete_pipeline(
    pipeline_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    '''Удалить пайплайн'''

    await validate_pipeline_id(pipeline_id, session)
    return await pipeline_crud.delete_by_id(
        session,
        pipeline_id
    )

@router.get(
    '/{pipeline_id}/versions',
    status_code=status.HTTP_200_OK,
    response_model=list[PipelineVersionRead],
    summary='Получить список версий пайплайна',
    description='Получить список версий пайплайна'
)
async def get_pipeline_versions(
    pipeline_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить список версий пайплайна'''

    await validate_pipeline_id(pipeline_id, session)
    return await pipeline_version_crud.get_all_by_pipeline_id(
        session,
        pipeline_id
    )