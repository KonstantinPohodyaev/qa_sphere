'''
Модель User
'''
import uuid
from enum import StrEnum
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.annotations import GUID
from models.base import BaseModel

if TYPE_CHECKING:
    from models.pipeline import Pipeline
    from models.pipeline_run import PipelineRun


class UserRole(StrEnum):
    '''Роли пользователей'''

    ADMIN = 'admin'
    USER = 'user'


class User(BaseModel):
    '''Модель пользователя'''
    
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.USER,
        nullable=False
    )
    
    # Relationships
    pipelines: Mapped[List['Pipeline']] = relationship(
        'Pipeline',
        secondary='pipeline_owners',
        back_populates='owners'
    )
    pipeline_runs: Mapped[List['PipelineRun']] = relationship(
        'PipelineRun',
        back_populates='user'
    )