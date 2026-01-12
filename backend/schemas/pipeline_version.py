'''
Pydantic схемы для PipelineVersion
'''
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PipelineVersionBase(BaseModel):
    '''Базовая схема для PipelineVersion'''
    pipeline_id: uuid.UUID
    version: str
    schema: Optional[dict] = None
    description: Optional[str] = None
    is_active: bool = True

    class Config:
        title = 'PipelineVersionBase'


class PipelineVersion(BaseModel):
    '''Схема PipelineVersion'''
    id: uuid.UUID
    pipeline_id: uuid.UUID
    version: str
    schema: Optional[dict] = None
    description: Optional[str] = None
    is_active: bool = True

class PipelineVersionCreate(BaseModel):
    '''Схема для создания PipelineVersion'''
    version: str
    schema: Optional[dict] = None
    description: Optional[str] = None
    is_active: bool = True


class PipelineVersionUpdate(BaseModel):
    '''Схема для обновления PipelineVersion'''
    version: Optional[str] = None
    schema: Optional[dict] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PipelineVersionInDB(PipelineVersionBase):
    '''Схема PipelineVersion из базы данных'''
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        title = 'PipelineVersionInDB'
        from_attributes = True


class PipelineVersionRead(PipelineVersionInDB):
    '''Схема PipelineVersion для ответа API'''
    pass
