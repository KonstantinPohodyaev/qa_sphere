'''
Валидаторы для Pipeline
'''
from crud.pipeline import pipeline_crud
from database.base import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status


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
