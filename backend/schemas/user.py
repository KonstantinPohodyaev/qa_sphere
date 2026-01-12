'''
Pydantic схемы для User
'''
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from models.user import UserRole


class UserBase(BaseModel):
    '''Базовая схема для User'''
    email: EmailStr
    is_active: bool = True
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    '''Схема для создания User'''
    password: str


class UserUpdate(BaseModel):
    '''Схема для обновления User'''
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    pipelines: Optional[list[dict]] = None


class UserPipelinesRead(BaseModel):
    '''Схема для списка пайплайнов пользователя'''
    id: uuid.UUID
    name: str
    code: str
    description: Optional[str] = None
    executor_type: str
    external_id: Optional[str] = None
    is_active: bool = True


class UserInDB(UserBase):
    '''Схема User из базы данных'''
    id: uuid.UUID | str
    password_hash: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    '''Схема User для ответа API (без пароля)'''
    id: uuid.UUID
    created_at: datetime
    pipelines: Optional[list[UserPipelinesRead]] = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    '''Схема для логина пользователя'''
    email: EmailStr
    password: str


class Token(BaseModel):
    '''Схема для JWT токена'''
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    '''Данные из JWT токена'''
    user_id: Optional[uuid.UUID] = None
