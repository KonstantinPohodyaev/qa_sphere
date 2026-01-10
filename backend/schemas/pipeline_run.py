'''
Pydantic схемы для PipelineRun
'''
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from models.pipeline_run import PipelineRunStatus


class PipelineRunBase(BaseModel):
    '''Базовая схема для PipelineRun'''
    pipeline_id: uuid.UUID
    pipeline_version_id: uuid.UUID
    status: PipelineRunStatus = PipelineRunStatus.PENDING
    executor_run_id: Optional[str] = None
    
    class Config:
        title = 'PipelineRunBase'


class PipelineRunCreate(BaseModel):
    '''Схема для создания PipelineRun'''
    pipeline_version_id: uuid.UUID
    
    class Config:
        title = 'PipelineRunCreate'


class PipelineRunUpdate(BaseModel):
    '''Схема для обновления PipelineRun'''
    status: Optional[PipelineRunStatus] = None
    executor_run_id: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    
    class Config:
        title = 'PipelineRunUpdate'


class PipelineRunInDB(PipelineRunBase):
    '''Схема PipelineRun из базы данных'''
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        title = 'PipelineRunInDB'
        from_attributes = True


class PipelineRun(PipelineRunInDB):
    '''Схема PipelineRun для ответа API'''
    
    class Config:
        title = 'PipelineRun'
        from_attributes = True
