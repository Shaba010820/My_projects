from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int = Field(default=1, ge=0)
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None


class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
