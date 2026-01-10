'''
Модель Pipeline
'''
import uuid
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator, CHAR

from models.base import BaseModel
from database.annotations import GUID

if TYPE_CHECKING:
    from models.pipeline_version import PipelineVersion
    from models.pipeline_run import PipelineRun
    from models.user import User

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
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    executor_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
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
    user: Mapped['User'] = relationship('User', back_populates='pipelines')
