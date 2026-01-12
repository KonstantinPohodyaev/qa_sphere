import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.annotations import GUID, not_null_unique_str
from models.base import BaseModel

if TYPE_CHECKING:
    from models.pipeline_run import PipelineRun


class RunParamValue(BaseModel):
    '''Модель значения параметра запуска'''
    
    pipeline_run_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey('pipelineruns.id', ondelete='CASCADE'),
        nullable=False,
    )
    name: Mapped[not_null_unique_str]
    value: Mapped[str] = mapped_column(Text, nullable=False)

    pipeline_run: Mapped['PipelineRun'] = relationship(
        'PipelineRun',
        back_populates='param_values',
    )
