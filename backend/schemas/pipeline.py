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


class PipelineInDB(PipelineBase):
    '''Схема Pipeline из базы данных'''
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class Pipeline(PipelineInDB):
    '''Схема Pipeline для ответа API'''
    pass
