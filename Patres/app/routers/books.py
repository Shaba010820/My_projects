from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.books import Book
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.books import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookRead, status_code=201)
def create_books(
    book: BookCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing:
        raise HTTPException(
            status_code=400, detail="Book with this ISBN already exists"
        )

    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@router.get("/", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()

    return books


@router.get("/{book_id}", response_model=BookRead)
def get_book(
    book_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book is not found")

    return book


@router.put("/{book_id}", response_model=BookRead)
def update_books(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book is not found")
    for field, value in book_update.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_books(
    book_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book is not found")

    db.delete(book)
    db.commit()

    return None
