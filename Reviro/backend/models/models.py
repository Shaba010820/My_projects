from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy import Enum as SQLEnum
from enum import Enum


class BaseModel(DeclarativeBase):
    ...


class TaskStatus(str, Enum):
    new = 'new'
    in_progress = 'in_progress'
    done = 'done'


class Task(BaseModel):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    due_date: Mapped[datetime] = mapped_column(DateTime())
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus, name='task_status'))
