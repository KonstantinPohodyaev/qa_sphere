'''
Pydantic схемы для RunParamValue
'''
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RunParamValueBase(BaseModel):
    '''Базовая схема для RunParamValue'''
    name: str
    value: str
    
    class Config:
        title = 'RunParamValueBase'


class RunParamValueCreate(BaseModel):
    '''Схема для создания RunParamValue'''
    name: str
    value: str
    
    class Config:
        title = 'RunParamValueCreate'


class RunParamValueUpdate(BaseModel):
    '''Схема для обновления RunParamValue'''
    name: Optional[str] = None
    value: Optional[str] = None
    
    class Config:
        title = 'RunParamValueUpdate'


class RunParamValueInDB(RunParamValueBase):
    '''Схема RunParamValue из базы данных'''
    id: uuid.UUID
    pipeline_run_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        title = 'RunParamValueInDB'
        from_attributes = True


class RunParamValueRead(RunParamValueInDB):
    '''Схема RunParamValue для ответа API'''
    
    class Config:
        title = 'RunParamValue'
        from_attributes = True
