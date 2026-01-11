'''
Базовый CRUD класс (асинхронный)
'''
import uuid
from typing import Generic, TypeVar, Type, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from models.base import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType')
UpdateSchemaType = TypeVar('UpdateSchemaType')

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    '''Базовый CRUD класс'''

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        **filters
    ) -> list[ModelType]:
        '''Получить все модели с опциональными фильтрами'''
        query = select(self.model)

        # Применяем фильтры
        for key, value in filters.items():
            if hasattr(self.model, key) and value is not None:
                query = query.where(getattr(self.model, key) == value)
        
        result = await session.execute(
            query.offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_id(
        self,
        session: AsyncSession,
        id: uuid.UUID
    ) -> Optional[ModelType]:
        '''Получить модель по ID'''

        return (
            await session.execute(
                select(self.model).where(self.model.id == id)
            )
        ).scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        create_schema: CreateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        '''Создать модель'''
        try:
            db_object = self.model(**create_schema.model_dump())
            session.add(db_object)
            if commit:
                await session.commit()
                await session.refresh(db_object)
            return db_object
        except IntegrityError as error:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail=f'Ошибка целостности данных: {str(error)}'
            )
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f'Ошибка SQLAlchemy: {str(error)}'
            )

    async def update(
        self,
        session: AsyncSession,
        db_object: ModelType,
        update_schema: UpdateSchemaType,
        commit: bool = True,
    ) -> ModelType:
        '''Обновить модель'''
        try:
            # Поддержка как Pydantic схем, так и dict
            update_data = update_schema.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_object, field, value)
            session.add(db_object)
            if commit:
                await session.commit()
                await session.refresh(db_object)
            return db_object
        except IntegrityError as error:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail=f'Ошибка целостности данных: {str(error)}'
            )
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f'Ошибка SQLAlchemy: {str(error)}'
            )

    async def delete(
        self,
        session: AsyncSession,
        db_object: ModelType,
        commit: bool = True,
    ) -> ModelType:
        '''Удалить модель'''
        try:
            await session.delete(db_object)
            if commit:
                await session.commit()
            return db_object
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f'Ошибка SQLAlchemy: {str(error)}'
            )
    
    async def delete_by_id(
        self,
        session: AsyncSession,
        id: uuid.UUID,
        commit: bool = True,
    ) -> bool:
        '''Удалить модель по ID'''
        try:
            db_object = await self.get_by_id(session, id)
            if not db_object:
                return False
            await session.delete(db_object)
            if commit:
                await session.commit()
            return True
        except SQLAlchemyError as error:
            await session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f'Ошибка SQLAlchemy: {str(error)}'
            )
