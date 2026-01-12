'''
Модель Pipeline
'''
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import CHAR, TypeDecorator

from database.annotations import GUID, null_text
from database.base import Base
from models.base import BaseModel

if TYPE_CHECKING:
    from models.pipeline_run import PipelineRun
    from models.pipeline_version import PipelineVersion
    from models.user import User

# Ассоциативная таблица для связи многие-ко-многим между Pipeline и User
pipeline_owners = Table(
    'pipeline_owners',
    Base.metadata,
    Column('pipeline_id', GUID(), ForeignKey('pipelines.id', ondelete='CASCADE'), primary_key=True),
    Column('user_id', GUID(), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
)

class Pipeline(BaseModel):
    '''Модель Pipeline'''
    
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    description: Mapped[null_text]
    executor_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    versions: Mapped[List['PipelineVersion']] = relationship(
        'PipelineVersion',
        back_populates='pipeline',
        cascade='all, delete-orphan'
    )
    runs: Mapped[List['PipelineRun']] = relationship(
        'PipelineRun',
        back_populates='pipeline',
        cascade='all, delete-orphan'
    )
    owners: Mapped[List['User']] = relationship(
        'User',
        secondary=pipeline_owners,
        back_populates='pipelines'
    )
