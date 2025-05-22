import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.session import get_db
from app.models.books import Book
from app.models.readers import Reader
from app.models.user import Base
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def register_and_login(client):
    user_data = {"email": "test@example.com", "password": "testpass"}
    client.post("/auth/register", json=user_data)
    resp = client.post(
        "/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    assert resp.status_code == 200, f"Login failed: {resp.status_code} {resp.text}"
    access_token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_book_and_reader(db: Session):
    book = Book(title="Book", author="Author", copies=3)
    email = f"reader_{uuid.uuid4()}@example.com"
    reader = Reader(name="Reader", email=email)
    db.add(book)
    db.add(reader)
    db.commit()
    db.refresh(book)
    db.refresh(reader)
    return book, reader


@pytest.fixture
def create_reader(db: Session):
    email = f"reader_{uuid.uuid4()}@example.com"
    reader = Reader(name="Shaba", email=email)
    db.add(reader)
    db.commit()
    db.refresh(reader)

    return reader
