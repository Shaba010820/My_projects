from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BorrowBookRequest(BaseModel):
    book_id: int
    reader_id: int


class ReturnBookRequest(BaseModel):
    borrow_id: int
    reader_id: int


class BorrowedBookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
