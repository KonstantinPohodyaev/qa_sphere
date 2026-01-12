'''
Валидаторы для Pipeline
'''
import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.pipeline import pipeline_crud
from database.base import get_async_session


async def validate_pipeline_code(
    code: str, session: AsyncSession = Depends(get_async_session)
):
    '''Валидация кода пайплайна'''
    pipeline = await pipeline_crud.get_by_code(session, code)
    if pipeline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пайплайн с кодом = {code} уже существует'
        )
    return pipeline


async def validate_pipeline_name(
    name: str, session: AsyncSession = Depends(get_async_session)
):
    '''Валидация названия пайплайна'''
    pipeline = await pipeline_crud.get_by_name(session, name)
    if pipeline:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пайплайн с названием = {name} уже существует'
        )


async def validate_pipeline_id(
    pipeline_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
):
    '''Валидация ID пайплайна'''

    pipeline = await pipeline_crud.get_by_id(session, pipeline_id)
    if not pipeline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Пайплайн с ID = {pipeline_id} не существует'
        )
    return pipeline