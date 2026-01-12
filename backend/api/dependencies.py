'''
Зависимости для API (dependencies)
'''
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_user_id_from_token
from crud.user import user_crud
from database.base import get_async_session
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def get_current_user_id(
    token: str = Depends(oauth2_scheme)
) -> uuid.UUID:
    '''
    Получить ID текущего пользователя из JWT токена
    
    Args:
        token: JWT токен из заголовка Authorization
    
    Returns:
        UUID пользователя
    
    Raises:
        HTTPException: Если токен недействителен или пользователь не найден
    '''
    user_id = get_user_id_from_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен доступа",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id


async def get_current_user(
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    '''
    Получить текущего пользователя из базы данных по JWT токену
    
    Args:
        user_id: ID пользователя из токена
        session: Сессия базы данных
    
    Returns:
        Объект пользователя
    
    Raises:
        HTTPException: Если пользователь не найден или неактивен
    '''
    user = await user_crud.get_current_user(session, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь неактивен"
        )
    
    return user
