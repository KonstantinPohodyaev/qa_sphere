'''
Pydantic схемы для Pipeline
'''
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PipelineBase(BaseModel):
    '''Базовая схема для Pipeline'''
    name: str
    code: str
    description: Optional[str] = None
    executor_type: str
    external_id: Optional[str] = None
    is_active: bool = True


class PipelineCreate(PipelineBase):
    '''Схема для создания Pipeline'''
    pass


class PipelineUpdate(BaseModel):
    '''Схема для обновления Pipeline'''
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    executor_type: Optional[str] = None
    external_id: Optional[str] = None
    is_active: Optional[bool] = None
    owners: Optional[list[dict]] = None  # Список словарей с ключом 'id' для owner_id


class PipelineInDB(PipelineBase):
    '''Схема Pipeline из базы данных'''
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PipelineUserRead(BaseModel):
    '''Схема пользователя для Pipeline'''
    id: uuid.UUID
    email: str
    is_active: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PipelineRead(PipelineInDB):
    '''Схема Pipeline для ответа API'''
    owners: list[PipelineUserRead] = []
    
    model_config = ConfigDict(from_attributes=True)


class PipelineReadShort(PipelineRead):
    '''Схема Pipeline для краткого ответа API'''
    
    pass
