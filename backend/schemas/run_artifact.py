'''
Pydantic схемы для RunArtifact
'''
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.run_artifact import TypeEnum


class RunArtifactBase(BaseModel):
    '''Базовая схема для RunArtifact'''
    name: str
    type: TypeEnum
    schema: Optional[dict] = None
    
    class Config:
        title = 'RunArtifactBase'


class RunArtifactCreate(BaseModel):
    '''Схема для создания RunArtifact'''
    name: str
    type: TypeEnum
    schema: Optional[dict] = None
    
    class Config:
        title = 'RunArtifactCreate'


class RunArtifactUpdate(BaseModel):
    '''Схема для обновления RunArtifact'''
    name: Optional[str] = None
    type: Optional[TypeEnum] = None
    schema: Optional[dict] = None
    
    class Config:
        title = 'RunArtifactUpdate'


class RunArtifactInDB(RunArtifactBase):
    '''Схема RunArtifact из базы данных'''
    id: uuid.UUID
    pipeline_run_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        title = 'RunArtifactInDB'
        from_attributes = True


class RunArtifact(RunArtifactInDB):
    '''Схема RunArtifact для ответа API'''
    
    class Config:
        title = 'RunArtifact'
        from_attributes = True
