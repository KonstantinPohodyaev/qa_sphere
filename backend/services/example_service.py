'''
Пример сервиса для работы с Example (асинхронный)
'''
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.example import Example
from schemas.example import ExampleCreate, ExampleUpdate


class ExampleService:
    '''Сервис для работы с Example'''
    
    @staticmethod
    async def get_by_id(db: AsyncSession, example_id: UUID) -> Optional[Example]:
        '''Получить Example по ID'''
        result = await db.execute(
            select(Example).where(Example.id == example_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> list[Example]:
        '''Получить все Example'''
        result = await db.execute(
            select(Example).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def create(db: AsyncSession, example: ExampleCreate) -> Example:
        '''Создать новый Example'''
        db_example = Example(**example.model_dump())
        db.add(db_example)
        await db.commit()
        await db.refresh(db_example)
        return db_example
    
    @staticmethod
    async def update(
        db: AsyncSession,
        example_id: UUID,
        example: ExampleUpdate
    ) -> Optional[Example]:
        '''Обновить Example'''
        db_example = await ExampleService.get_by_id(db, example_id)
        if not db_example:
            return None
        
        update_data = example.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_example, field, value)
        
        await db.commit()
        await db.refresh(db_example)
        return db_example
    
    @staticmethod
    async def delete(db: AsyncSession, example_id: UUID) -> bool:
        '''Удалить Example'''
        db_example = await ExampleService.get_by_id(db, example_id)
        if not db_example:
            return False
        
        await db.delete(db_example)
        await db.commit()
        return True
