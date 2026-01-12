'''
Базовые модели
'''
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from database.annotations import not_null_datetime
from database.base import Base


class BaseModel(Base):
    '''Базовый класс для всех моделей'''
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[not_null_datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[not_null_datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls):
        '''Автоматическая генерация имени таблицы из имени класса'''
        return cls.__name__.lower() + 's'
