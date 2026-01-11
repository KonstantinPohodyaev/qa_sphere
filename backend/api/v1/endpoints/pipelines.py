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
    response_model=list[PipelineRead],
    summary='Получить список всех пайплайнов',
    description='Получить список всех пайплайнов',
)
async def get_all_pipelines(
    offset: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить список всех пайплайнов'''
    return await pipeline_crud.get_all_pipelines(session, offset, limit)


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
    
    # Загружаем связанные данные пользователя для всех пайплайнов
    if pipelines_list:
        pipeline_ids = [p.id for p in pipelines_list]
        return (
            await session.execute(
                select(Pipeline)
                .where(Pipeline.id.in_(pipeline_ids))
                .options(selectinload(Pipeline.user))
            )
        ).scalars().all()
    return []


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
            .options(selectinload(Pipeline.user))
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
    return (
        await session.execute(
            select(Pipeline)
            .where(Pipeline.id == db_pipeline.id)
            .options(selectinload(Pipeline.user))
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
    db_pipeline = await pipeline_crud.get_by_id(session, pipeline_id)
    if not db_pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pipeline not found'
        )
    
    # Валидация уникальности code, если он обновляется
    if pipeline_data.code is not None and pipeline_data.code != db_pipeline.code:
        existing_pipeline = await pipeline_crud.get_by_code(session, pipeline_data.code)
        if existing_pipeline and existing_pipeline.id != pipeline_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пайплайн с кодом = {pipeline_data.code} уже существует'
            )
    
    # Валидация уникальности name, если он обновляется
    if pipeline_data.name is not None and pipeline_data.name != db_pipeline.name:
        existing_pipeline = await pipeline_crud.get_by_name(session, pipeline_data.name)
        if existing_pipeline and existing_pipeline.id != pipeline_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Пайплайн с названием = {pipeline_data.name} уже существует'
            )
    
    # Обновляем только переданные поля (exclude_unset=True уже используется в CRUDBase)
    db_pipeline = await pipeline_crud.update(
        session,
        db_pipeline,
        pipeline_data,
        commit=True
    )
    await session.refresh(db_pipeline, ['user'])
    return (
        await session.execute(
            select(Pipeline)
            .where(Pipeline.id == pipeline_id)
            .options(selectinload(Pipeline.user))
        )
    ).scalar_one_or_none()


@router.delete(
    '/{pipeline_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Удалить пайплайн',
    description='Удалить пайплайн по ID',
)
async def delete_pipeline(
    pipeline_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session)
):
    '''Удалить пайплайн'''
    success = await pipeline_crud.delete_by_id(
        session,
        pipeline_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pipeline not found'
        )
    return None
