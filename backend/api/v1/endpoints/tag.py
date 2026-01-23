from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_async_session
from crud.tag import tag_crud
from validators.tag import validate_tag_id
from schemas.tag import TagRead

router = APIRouter()

@router.get(
    '/tags',
    response_model=list[TagRead],
    status_code=status.HTTP_200_OK,
    summary='Получить все теги',
    description='Получить все теги',
)
async def get_all_tags(
    session: AsyncSession = Depends(get_async_session),
) -> list[TagRead]:
    '''Получить все теги'''

    return await tag_crud.get_all(session)


@router.get(
    '/tags/{tag_id}',
    response_model=TagRead,
    status_code=status.HTTP_200_OK,
    summary='Получить тег по ID',
    description='Получить тег по ID',
)
async def get_tag_by_id(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> TagRead:
    '''Получить тег по ID'''

    return await validate_tag_id(tag_id, session)
