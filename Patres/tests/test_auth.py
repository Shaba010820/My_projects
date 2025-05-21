from fastapi.testclient import TestClient


def test_register_user(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={"email": "newestuser@example.com", "password": "newpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data


def test_register_existing_user(client: TestClient) -> None:
    user_data = {"email": "duplicate@example.com", "password": "somepass"}

    response1 = client.post("/auth/register", json=user_data)
    assert response1.status_code == 201

    response2 = client.post("/auth/register", json=user_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()


def test_login_user(client: TestClient) -> None:
    client.post(
        "/auth/register",
        json={"email": "newuser@example.com", "password": "newpassword"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "newuser@example.com", "password": "newpassword"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        data={"username": "newuser@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient) -> None:
    response = client.post(
        "/auth/login", data={"username": "doesnotexist@example.com", "password": "any"}
    )
    assert response.status_code == 401
