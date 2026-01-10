import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from database.base import get_async_session
from crud.user import user_crud


async def validate_user_id(
    user_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    '''Валидация ID пользователя'''
    user = await user_crud.get_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Пользователя в UUID = {user_id} не существует'
        )
