'''
Эндпоинты для работы с Example
'''
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.base import get_db
from schemas.example import Example, ExampleCreate, ExampleUpdate
from services.example_service import ExampleService

router = APIRouter()


@router.get('/', response_model=List[Example])
def get_examples(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    '''Получить список всех Example'''
    examples = ExampleService.get_all(db, skip=skip, limit=limit)
    return examples


@router.get('/{example_id}', response_model=Example)
def get_example(
    example_id: int,
    db: Session = Depends(get_db)
):
    '''Получить Example по ID'''
    example = ExampleService.get_by_id(db, example_id)
    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Example not found'
        )
    return example


@router.post('/', response_model=Example, status_code=status.HTTP_201_CREATED)
def create_example(
    example: ExampleCreate,
    db: Session = Depends(get_db)
):
    '''Создать новый Example'''
    return ExampleService.create(db, example)


@router.put('/{example_id}', response_model=Example)
def update_example(
    example_id: int,
    example: ExampleUpdate,
    db: Session = Depends(get_db)
):
    '''Обновить Example'''
    updated_example = ExampleService.update(db, example_id, example)
    if not updated_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Example not found'
        )
    return updated_example


@router.delete('/{example_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_example(
    example_id: int,
    db: Session = Depends(get_db)
):
    '''Удалить Example'''
    if not ExampleService.delete(db, example_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Example not found'
        )
    return None
