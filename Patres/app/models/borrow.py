from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.user import Base


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(primary_key=True)

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(default=datetime.now)
    return_date: Mapped[datetime | None] = mapped_column(nullable=True)

    book = relationship("Book", backref="borrowed_books")
    reader = relationship("Reader", backref="borrowed_books")
