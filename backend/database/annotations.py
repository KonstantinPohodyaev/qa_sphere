'''
Кастомные типы данных для SQLAlchemy
'''
import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import CHAR, TypeDecorator

try:
    from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
except ImportError:
    PostgresUUID = None


class GUID(TypeDecorator):
    '''Универсальный тип для UUID (работает с SQLite и PostgreSQL)'''
    impl = CHAR
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql' and PostgresUUID:
            return dialect.type_descriptor(PostgresUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            return str(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

not_null_datetime = Annotated[datetime, mapped_column(nullable=False)]
not_null_unique_str = Annotated[str, mapped_column(String(255), nullable=False, unique=True)]
