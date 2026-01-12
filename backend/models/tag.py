from models.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum as SQLEnum, ForeignKey, UniqueConstraint
import uuid
from enum import StrEnum
from database.annotations import not_null_unique_str, GUID, null_text
from typing import Optional
from sqlalchemy import Text
from models.enums.tag import TagType


class Tag(BaseModel):
    '''Модель тега'''

    name: Mapped[not_null_unique_str]
    type: Mapped[TagType] = mapped_column(SQLEnum(TagType), nullable=False)
    description: Mapped[null_text]


class TagLink(BaseModel):
    '''Модель связи тега с объектом'''
    __tablename__ = 'tag_links'
    __table_args__ = (
        UniqueConstraint(
            'tag_id', 
            'entity_type', 
            'entity_id', 
            name='uix_tag_link_unique'
        ),
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey('tags.id'), nullable=False
    )
    entity_type: Mapped[str] = mapped_column(String(255), nullable=False)
    enntity_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)

    tag: Mapped['Tag'] = relationship('Tag', back_populates='links')
