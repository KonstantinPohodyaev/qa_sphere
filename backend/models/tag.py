import uuid
from typing import List

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.annotations import GUID, not_null_unique_str, null_text
from models.base import BaseModel
from models.enums.tag import TagType


class Tag(BaseModel):
    '''Модель тега'''

    name: Mapped[not_null_unique_str]
    type: Mapped[TagType] = mapped_column(SQLEnum(TagType), nullable=False)
    description: Mapped[null_text]

    # Relationships
    links: Mapped[List['TagLink']] = relationship('TagLink', back_populates='tag')


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
    entity_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)

    tag: Mapped['Tag'] = relationship('Tag', back_populates='links')
