import pytest
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_login():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "password"},  # form-data, не JSON!
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.fixture
def token():
    response = client.post(
        "/login",
        data={"username": "admin", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]



def test_protected_endpoint(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200