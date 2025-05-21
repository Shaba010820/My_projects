from fastapi.testclient import TestClient

from app.models.borrow import BorrowedBook


def test_borrow_book_success(
    client: TestClient, register_and_login, test_book_and_reader
) -> None:
    book, reader = test_book_and_reader

    response = client.post(
        "/borrow/",
        json={"book_id": book.id, "reader_id": reader.id},
        headers=register_and_login,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book.id
    assert data["reader_id"] == reader.id
    assert data["return_date"] is None


def test_borrow_book_unavailable(
    client: TestClient, register_and_login, db, test_book_and_reader
) -> None:
    book, reader = test_book_and_reader
    book.copies = 0
    db.commit()

    response = client.post(
        "/borrow/",
        json={"book_id": book.id, "reader_id": reader.id},
        headers=register_and_login,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Book is not available"


def test_borrow_book_max_limit(
    client: TestClient, register_and_login, db, test_book_and_reader
) -> None:
    book, reader = test_book_and_reader

    for _ in range(3):
        borrow = BorrowedBook(book_id=book.id, reader_id=reader.id)
        db.add(borrow)
    db.commit()

    response = client.post(
        "/borrow/",
        json={"book_id": book.id, "reader_id": reader.id},
        headers=register_and_login,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader has already borrowed 3 books"


def test_return_book_success(
    client: TestClient, register_and_login, db, test_book_and_reader
) -> None:
    book, reader = test_book_and_reader
    borrow = BorrowedBook(book_id=book.id, reader_id=reader.id)
    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    response = client.post(
        "/borrow/return", json={"borrow_id": borrow.id}, headers=register_and_login
    )

    assert response.status_code == 200
    assert response.json()["return_date"] is not None


def test_return_book_invalid_id(client: TestClient, register_and_login):
    response = client.post(
        "/borrow/return", json={"borrow_id": 9999}, headers=register_and_login
    )

    assert response.status_code == 400


def test_get_active_borrows(
    client: TestClient, register_and_login, db, test_book_and_reader
) -> None:
    book, reader = test_book_and_reader
    borrow = BorrowedBook(book_id=book.id, reader_id=reader.id)
    db.add(borrow)
    db.commit()

    response = client.get(f"/borrow/reader/{reader.id}", headers=register_and_login)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(b["id"] == borrow.id for b in data)
