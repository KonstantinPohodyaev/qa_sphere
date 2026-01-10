'''
Pydantic схемы для Pipeline
'''
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from schemas.user import UserRead


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
    user_id: uuid.UUID


class PipelineUpdate(BaseModel):
    '''Схема для обновления Pipeline'''
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    executor_type: Optional[str] = None
    external_id: Optional[str] = None
    user_id: Optional[uuid.UUID] = None
    is_active: Optional[bool] = None


class PipelineInDB(PipelineBase):
    '''Схема Pipeline из базы данных'''
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PipelineWithUser(PipelineInDB):
    '''Схема Pipeline с информацией о пользователе'''
    user: UserRead
    
    model_config = ConfigDict(from_attributes=True)


class PipelineRead(PipelineWithUser):
    '''Схема Pipeline для ответа API'''
    pass
