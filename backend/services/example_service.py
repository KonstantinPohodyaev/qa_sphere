'''
Пример сервиса для работы с Example
'''
from typing import List, Optional
from sqlalchemy.orm import Session

from models.example import Example
from schemas.example import ExampleCreate, ExampleUpdate


class ExampleService:
    '''Сервис для работы с Example'''
    
    @staticmethod
    def get_by_id(db: Session, example_id: int) -> Optional[Example]:
        '''Получить Example по ID'''
        return db.query(Example).filter(Example.id == example_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Example]:
        '''Получить все Example'''
        return db.query(Example).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, example: ExampleCreate) -> Example:
        '''Создать новый Example'''
        db_example = Example(**example.model_dump())
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        return db_example
    
    @staticmethod
    def update(db: Session, example_id: int, example: ExampleUpdate) -> Optional[Example]:
        '''Обновить Example'''
        db_example = ExampleService.get_by_id(db, example_id)
        if not db_example:
            return None
        
        update_data = example.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_example, field, value)
        
        db.commit()
        db.refresh(db_example)
        return db_example
    
    @staticmethod
    def delete(db: Session, example_id: int) -> bool:
        '''Удалить Example'''
        db_example = ExampleService.get_by_id(db, example_id)
        if not db_example:
            return False
        
        db.delete(db_example)
        db.commit()
        return True
