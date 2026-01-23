from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.tag import tag_crud
from models.tag import Tag

async def validate_tag_id(tag_id: int, session: AsyncSession) -> Tag:
    '''Валидация ID тега'''

    tag = await tag_crud.get_by_id(session, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='ID тега должно быть больше 0'
        )
    return tag
