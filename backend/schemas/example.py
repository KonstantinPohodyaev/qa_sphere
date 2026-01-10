'''
Примеры Pydantic схем
'''
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ExampleBase(BaseModel):
    '''Базовая схема для Example'''
    title: str
    description: Optional[str] = None


class ExampleCreate(ExampleBase):
    '''Схема для создания Example'''
    pass


class ExampleUpdate(BaseModel):
    '''Схема для обновления Example'''
    title: Optional[str] = None
    description: Optional[str] = None


class ExampleInDB(ExampleBase):
    '''Схема Example из базы данных'''
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class Example(ExampleInDB):
    '''Схема Example для ответа API'''
    pass
