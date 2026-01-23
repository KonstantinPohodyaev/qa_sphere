from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from database.annotations import not_null_datetime

class TagBase(BaseModel):
    '''Модель тега'''

    id: int
    name: str
    description: str
    created_at: not_null_datetime
    updated_at: not_null_datetime


class TagCreate(TagBase):
    '''Модель создания тега'''

    name: str
    description: str

class TagUpdate(TagBase):
    '''Модель обновления тега'''

    name: Optional[str] = None
    description: Optional[str] = None

class TagRead(TagBase):
    '''Модель чтения тега'''

    id: int
    name: str
    description: str
    created_at: not_null_datetime
    updated_at: not_null_datetime
