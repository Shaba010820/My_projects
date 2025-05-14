from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.models import Task
from backend.schemas.crud import TaskCreate, TaskRead, TaskUpdate, TaskFilter
from .auth import verify_token

router = APIRouter(prefix='/tasks', tags=['CRUD-Operations'])

@router.get('/', response_model=List[TaskRead], status_code=200)
def get_tasks(
        task_filter: TaskFilter = Depends(TaskFilter),
        db: Session = Depends(get_db),
        token_data: dict = Depends(verify_token)
):
    return task_filter.filter(db.query(Task)).all()


@router.post('/', response_model=TaskRead, status_code=201)
def create_tasks(tasks: TaskCreate, db: Session = Depends(get_db),
                 token_data: dict = Depends(verify_token)):
    db_tasks = Task(**tasks.model_dump())
    db.add(db_tasks)
    db.commit()
    db.refresh(db_tasks)

    return db_tasks


@router.get('/{task_id}', response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db),
             token_data: dict = Depends(verify_token)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Элемента с таким айди нет')

    return task

@router.put('/{task_id}', response_model=TaskRead)
def update_task(task_id: int, updated: TaskCreate, db: Session = Depends(get_db),
                token_data: dict = Depends(verify_token)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Элемента с таким айди нет')

    task.title = updated.title
    task.description = updated.description
    task.due_date = updated.due_date
    task.status = updated.status

    db.commit()
    db.refresh(task)

    return task


@router.patch('/{task_id}', response_model=TaskRead)
def patch_task(task_id: int, updated: TaskUpdate, db: Session = Depends(get_db),
               token_data: dict = Depends(verify_token)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail='Элемента с таким айди нет')

    if updated.title is not None:
        task.title = updated.title
    if updated.description is not None:
        task.description = updated.description
    if updated.due_date is not None:
        task.due_date = updated.due_date
    if updated.status is not None:
        task.status = updated.status

    db.commit()
    db.refresh(task)

    return task

@router.delete('/{task_id}', status_code=204)
def delete_task(task_id: int, db:Session = Depends(get_db),
                token_data: dict = Depends(verify_token)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail='Элемента с таким айди нет')

    db.delete(task)
    db.commit()

    return Response(status_code=204)
