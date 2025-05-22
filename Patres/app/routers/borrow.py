from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.books import Book
from app.models.borrow import BorrowedBook
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.borrow import BorrowBookRequest, BorrowedBookRead, ReturnBookRequest

router = APIRouter(prefix="/borrow", tags=["borrowed"])


@router.post("/", response_model=BorrowedBookRead)
def borrow_book(
    request: BorrowBookRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == request.book_id).first()
    if not book or book.copies < 1:
        raise HTTPException(status_code=400, detail="Book is not available")

    active_borrows = (
        db.query(BorrowedBook)
        .filter(
            BorrowedBook.reader_id == request.reader_id,
            BorrowedBook.return_date.is_(None),
        )
        .count()
    )

    if active_borrows >= 3:
        raise HTTPException(
            status_code=404, detail="Reader has already borrowed 3 books"
        )

    borrow = BorrowedBook(book_id=request.book_id, reader_id=request.reader_id)

    book.copies -= 1

    db.add(borrow)
    db.commit()
    db.refresh(book)

    return borrow


@router.post("/return", response_model=BorrowedBookRead)
def return_book(
    request: ReturnBookRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    borrow = db.query(BorrowedBook).filter(BorrowedBook.id == request.borrow_id).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    if borrow.reader_id != request.reader_id:
        raise HTTPException(
            status_code=403, detail="This book was not borrowed by the given reader"
        )

    book = db.query(Book).filter(Book.id == borrow.book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    borrow.return_date = datetime.now()
    book.copies += 1

    db.commit()
    db.refresh(borrow)

    return borrow


@router.get("/reader/{reader_id}", response_model=list[BorrowedBookRead])
def get_active_borrowed_books(
    reader_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    borrows = (
        db.query(BorrowedBook)
        .filter(BorrowedBook.reader_id == reader_id, BorrowedBook.return_date.is_(None))
        .all()
    )

    return borrows
