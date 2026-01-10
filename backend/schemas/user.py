'''
Pydantic схемы для User
'''
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
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


class UserInDB(UserBase):
    '''Схема User из базы данных'''
    id: uuid.UUID
    password_hash: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    '''Схема User для ответа API (без пароля)'''
    id: uuid.UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
