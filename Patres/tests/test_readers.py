import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.readers import Reader


def unique_email() -> str:
    return f"reader_{uuid.uuid4()}@example.com"


def test_create_reader_success(client: TestClient, register_and_login) -> None:
    payload = {"name": "Test Reader", "email": unique_email()}
    response = client.post("/readers/", json=payload, headers=register_and_login)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


def test_create_reader_duplicate_email(
    client: TestClient, register_and_login, db: Session
) -> None:
    email = unique_email()
    reader = Reader(name="Existing", email=email)
    db.add(reader)
    db.commit()

    payload = {"name": "Duplicate", "email": email}
    response = client.post("/readers/", json=payload, headers=register_and_login)
    assert response.status_code == 400
    assert response.json()["detail"] == "Reader with this email already exists"


def test_list_readers(client: TestClient, register_and_login) -> None:
    response = client.get("/readers/", headers=register_and_login)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_reader_by_id(client, register_and_login, db):
    reader = Reader(name="Get Reader", email=unique_email())
    db.add(reader)
    db.commit()
    db.refresh(reader)

    response = client.get(f"/readers/{reader.id}", headers=register_and_login)
    assert response.status_code == 200
    assert response.json()["id"] == reader.id


def test_get_reader_not_found(client, register_and_login):
    response = client.get("/readers/9999", headers=register_and_login)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found"


def test_update_reader(client: TestClient, register_and_login, db) -> None:
    reader = Reader(name="Old Name", email=unique_email())
    db.add(reader)
    db.commit()
    db.refresh(reader)

    payload = {"name": "Updated Name"}
    response = client.put(
        f"/readers/{reader.id}", json=payload, headers=register_and_login
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_reader_not_found(client: TestClient, register_and_login) -> None:
    response = client.put(
        "/readers/9999", json={"name": "Nope"}, headers=register_and_login
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found"


def test_delete_reader(client: TestClient, register_and_login, db) -> None:
    reader = Reader(name="Delete Me", email=unique_email())
    db.add(reader)
    db.commit()
    db.refresh(reader)

    response = client.delete(f"/readers/{reader.id}", headers=register_and_login)
    assert response.status_code == 204

    deleted = db.query(Reader).filter(Reader.id == reader.id).first()
    assert deleted is None


def test_delete_reader_not_found(client: TestClient, register_and_login) -> None:
    response = client.delete("/readers/9999", headers=register_and_login)
    assert response.status_code == 404
    assert response.json()["detail"] == "Reader not found"
