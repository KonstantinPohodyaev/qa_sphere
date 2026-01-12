import uuid
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.annotations import GUID, not_null_unique_str
from models.base import BaseModel

if TYPE_CHECKING:
    from models.pipeline_run import PipelineRun


class TypeEnum(StrEnum):
    '''Типы артефактов'''
    FILE = 'file'
    LINK = 'link'
    TEXT = 'text'
    JSON = 'json'


class RunArtifact(BaseModel):
    '''Модель артефакта запуска'''

    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey('pipelineruns.id', ondelete='CASCADE'),
        nullable=False,
    )
    type: Mapped[TypeEnum] = mapped_column(
        SQLEnum(TypeEnum),
        nullable=False,
    )
    name: Mapped[not_null_unique_str]
    schema: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    pipeline_run: Mapped['PipelineRun'] = relationship(
        'PipelineRun',
        back_populates='artifacts',
    )
