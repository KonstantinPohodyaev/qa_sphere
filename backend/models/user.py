'''
Модель User
'''
import uuid
from typing import TYPE_CHECKING, List
from enum import StrEnum
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel
from database.annotations import GUID

if TYPE_CHECKING:
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
    pipeline_runs: Mapped[List['PipelineRun']] = relationship(
        'PipelineRun',
        back_populates='user'
    )