import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.session import engine
from datetime import datetime, timedelta
from backend.main import BaseModel
client = TestClient(app)


def get_access_token():
    response = client.post("/login", data={"username": "admin", "password": "password"})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def clear_db():
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    yield
    BaseModel.metadata.drop_all(bind=engine)


def create_sample_tasks():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Test Task",
        "description": "Description",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "status": "new"
    }
    response = client.post("/tasks/", json=data, headers=headers)
    assert response.status_code == 201
    return response.json()

# Тесты
def test_create_tasks():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Sample Task",
        "description": "Some description",
        "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "status": "new"
    }
    response = client.post("/tasks/", json=data, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Sample Task"

def test_get_tasks():
    task = create_sample_tasks()
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/tasks/{task['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == task["id"]

def test_get_tasks_not_found():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/tasks/999", headers=headers)
    assert response.status_code == 404

def test_update_tasks():
    task = create_sample_tasks()
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    updated = {
        "title": "Updated",
        "description": "Updated desc",
        "due_date": (datetime.now() + timedelta(days=2)).isoformat(),
        "status": "in_progress"
    }
    response = client.put(f"/tasks/{task['id']}", json=updated, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"

def test_patch_tasks():
    task = create_sample_tasks()
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    partial = {"status": "done"}
    response = client.patch(f"/tasks/{task['id']}", json=partial, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "done"

def test_delete_tasks():
    task = create_sample_tasks()
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/tasks/{task['id']}", headers=headers)
    assert response.status_code == 204
    get_resp = client.get(f"/tasks/{task['id']}", headers=headers)
    assert get_resp.status_code == 404

def test_filter_tasks():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    client.post("/tasks/", json={
        "title": "New task",
        "description": "desc",
        "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "status": "new"
    }, headers=headers)
    client.post("/tasks/", json={
        "title": "Done task",
        "description": "desc",
        "due_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "status": "done"
    }, headers=headers)

    response = client.get("/tasks/?status=done", headers=headers)
    assert response.status_code == 200
    for task in response.json():
        assert task["status"] == "done"
