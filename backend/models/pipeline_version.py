'''
Модель PipelineVersion
'''
import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from models.base import BaseModel
from database.annotations import GUID


if TYPE_CHECKING:
    from models.pipeline import Pipeline
    from models.pipeline_run import PipelineRun


class PipelineVersion(BaseModel):
    '''Модель версии пайплайна'''
    
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
    version: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    schema: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    pipeline: Mapped['Pipeline'] = relationship('Pipeline', back_populates='versions')
    runs: Mapped[list['PipelineRun']] = relationship(
        'PipelineRun',
        back_populates='pipeline_version',
        cascade='all, delete-orphan'
    )