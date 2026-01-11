'''
Утилиты для работы с безопасностью (хеширование паролей и JWT токены)
'''
from datetime import datetime, timedelta
from typing import Optional
import uuid
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    '''Хеширование пароля'''
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверка пароля'''
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    '''
    Создать JWT токен доступа
    
    Args:
        data: Данные для включения в токен (например, {"sub": user_id})
        expires_delta: Время жизни токена (по умолчанию используется из настроек)
    
    Returns:
        Закодированный JWT токен
    '''
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    '''
    Декодировать и проверить JWT токен
    
    Args:
        token: JWT токен для декодирования
    
    Returns:
        Декодированные данные токена или None, если токен недействителен
    '''
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[uuid.UUID]:
    '''
    Получить ID пользователя из JWT токена
    
    Args:
        token: JWT токен
    
    Returns:
        UUID пользователя или None, если токен недействителен
    '''
    payload = decode_access_token(token)
    if payload is None:
        return None

    user_id_str: str = payload.get("sub")
    if user_id_str is None:
        return None

    try:
        return uuid.UUID(user_id_str)
    except (ValueError, TypeError):
        return None
