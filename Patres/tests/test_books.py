from fastapi.testclient import TestClient


def test_create_book(client: TestClient, register_and_login) -> None:
    response = client.post(
        "/books/",
        json={
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "year": 1925,
            "isbn": "9780141182636",
            "copies": 3,
        },
        headers=register_and_login,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "The Great Gatsby"
    assert data["copies"] == 3
    assert "id" in data


def test_get_books(client, register_and_login):
    response = client.get("/books/", headers=register_and_login)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_single_book(client, register_and_login):
    books = client.get("/books/", headers=register_and_login).json()
    book_id = books[0]["id"]

    response = client.get(f"/books/{book_id}", headers=register_and_login)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id


def test_update_book(client, register_and_login):
    books = client.get("/books/", headers=register_and_login).json()
    book_id = books[0]["id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "Updated Title",
            "author": "Updated Author",
            "year": 2000,
            "isbn": "9999999999",
            "copies": 2,
        },
        headers=register_and_login,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["copies"] == 2


def test_delete_book(client, register_and_login):
    response = client.post(
        "/books/",
        json={"title": "Delete Me", "author": "Author", "copies": 1},
        headers=register_and_login,
    )
    book_id = response.json()["id"]

    response = client.delete(f"/books/{book_id}", headers=register_and_login)
    assert response.status_code == 204

    response = client.get(f"/books/{book_id}", headers=register_and_login)
    assert response.status_code == 404
