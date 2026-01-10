'''
Модель PipelineRun
'''
import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum as PyEnum

from sqlalchemy import String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.annotations import GUID
from models.base import BaseModel

if TYPE_CHECKING:
    from models.pipeline import Pipeline
    from models.pipeline_version import PipelineVersion
    from models.user import User
    from models.run_artifact import RunArtifact


class PipelineRunStatus(PyEnum):
    '''Статусы запусков пайплайна'''
    PENDING = 'pending'
    RUNNING = 'running'
    SUCCESS = 'success'
    FAILED = 'failed'


class PipelineRun(BaseModel):
    '''Модель запусков пайплайна'''
    
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    pipeline_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey('pipelines.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    pipeline_version_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey('pipelineversions.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    status: Mapped[PipelineRunStatus] = mapped_column(
        SQLEnum(PipelineRunStatus),
        default=PipelineRunStatus.PENDING,
        nullable=False,
        index=True
    )
    executor_run_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    pipeline: Mapped['Pipeline'] = relationship('Pipeline', back_populates='runs')
    pipeline_version: Mapped['PipelineVersion'] = relationship('PipelineVersion', back_populates='runs')
    user: Mapped[Optional['User']] = relationship('User', back_populates='pipeline_runs')
    artifacts: Mapped[list['RunArtifact']] = relationship('RunArtifact', back_populates='pipeline_run')
