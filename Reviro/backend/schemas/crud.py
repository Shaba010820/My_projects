from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from backend.models.models import Task, TaskStatus


class TaskFilter(Filter):
    status: Optional[TaskStatus] = None
    due_date__lt: Optional[datetime] = None
    due_date__gt: Optional[datetime] = None

    class Constants(Filter.Constants):
        model = Task


class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    status: TaskStatus


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str
    due_date: datetime
    status: TaskStatus


class UserCreate(BaseModel):
    username: str
    password: str
