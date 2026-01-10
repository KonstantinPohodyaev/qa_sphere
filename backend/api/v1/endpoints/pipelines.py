'''
Эндпоинты для работы с Pipeline
'''
import uuid
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.base import get_async_session
from schemas.pipeline import PipelineRead, PipelineCreate, PipelineUpdate
from crud.pipeline import pipeline_crud
from models.pipeline import Pipeline
from sqlalchemy import select

from api.validators.user import validate_user_id
from api.validators.pipeline import validate_pipeline_code, validate_pipeline_name

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[PipelineRead],
    summary='Получить список пайплайнов',
    description='Получить список пайплайнов текущего пользователя',
)
async def get_pipelines(
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
    
    # Загружаем связанные данные пользователя для всех пайплайнов
    if pipelines_list:
        pipeline_ids = [p.id for p in pipelines_list]
        return await session.execute(
            select(Pipeline)
            .where(Pipeline.id.in_(pipeline_ids))
            .options(selectinload(Pipeline.user))
        ).scalars().all()
    return []


@router.get(
    '/{pipeline_id}',
    status_code=status.HTTP_200_OK,
    response_model=PipelineRead,
    summary='Получить пайплайн по ID',
    description='Получить пайплайн по ID с проверкой владельца',
)
async def get_pipeline(
    pipeline_id: uuid.UUID,
    user_id: uuid.UUID,  # TODO: Получать из токена/сессии
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить пайплайн по ID'''
    db_pipeline = await pipeline_crud.get_by_id_with_user(
        session,
        pipeline_id=pipeline_id,
        user_id=user_id
    )
    if not db_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pipeline not found or access denied'
        )
    return await s(ession.execute(
        select(Pipeline)
        .where(Pipeline.id == pipeline_id)
        .where(Pipeline.user_id == user_id)
        .options(selectinload(Pipeline.user))
    )).scalar_one_or_none()


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

    # Убеждаемся, что user_id в схеме соответствует текущему пользователю
    if pipeline_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Cannot create pipeline for another user'
        )

    db_pipeline = await pipeline_crud.create_for_user(
        session,
        create_schema=pipeline_data,
        user_id=user_id
    )
    await session.refresh(db_pipeline, ['user'])
    return (await session.execute(
        select(Pipeline)
        .where(Pipeline.id == db_pipeline.id)
        .options(selectinload(Pipeline.user))
    )).scalar_one_or_none()


@router.put(
    '/{pipeline_id}',
    status_code=status.HTTP_200_OK,
    response_model=PipelineRead,
    summary='Обновить пайплайн',
    description='Обновить пайплайн с проверкой владельца',
)
async def update_pipeline(
    pipeline_id: uuid.UUID,
    pipeline_data: PipelineUpdate,
    user_id: uuid.UUID,  # TODO: Получать из токена/сессии
    session: AsyncSession = Depends(get_async_session)
):
    '''Обновить пайплайн'''
    # Если пытаются изменить user_id, проверяем права
    if pipeline_data.user_id is not None and pipeline_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Cannot transfer pipeline to another user'
        )
    
    db_pipeline = await pipeline_crud.update_for_user(
        session,
        pipeline_id=pipeline_id,
        user_id=user_id,
        update_schema=pipeline_data
    )
    if not db_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pipeline not found or access denied'
        )
    await session.refresh(db_pipeline, ['user'])
    return await (session.execute(
        select(Pipeline)
        .where(Pipeline.id == pipeline_id)
        .where(Pipeline.user_id == user_id)
        .options(selectinload(Pipeline.user))
    )).scalar_one_or_none()


@router.delete(
    '/{pipeline_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить пайплайн',
    description='Удалить пайплайн с проверкой владельца',
)
async def delete_pipeline(
    pipeline_id: uuid.UUID,
    user_id: uuid.UUID,  # TODO: Получать из токена/сессии
    session: AsyncSession = Depends(get_async_session)
):
    '''Удалить пайплайн'''
    success = await pipeline_crud.delete_for_user(
        session,
        pipeline_id=pipeline_id,
        user_id=user_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pipeline not found or access denied'
        )
    return None
