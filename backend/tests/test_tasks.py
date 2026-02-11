import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


@pytest.fixture
def auth_token():
    """Fixture to create a user and return auth token"""
    response = client.post(
        "/api/auth/signup",
        json={"email": "taskuser@example.com", "password": "testpass123"}
    )
    return response.json()["data"]["token"]


def test_create_task_success(auth_token):
    """Test successful task creation"""
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Test Task"
    assert data["data"]["completed"] is False


def test_create_task_without_auth():
    """Test task creation without authentication"""
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task"}
    )
    assert response.status_code == 403


def test_create_task_empty_title(auth_token):
    """Test task creation with empty title"""
    response = client.post(
        "/api/tasks",
        json={"title": ""},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400


def test_list_tasks(auth_token):
    """Test listing user's tasks"""
    # Create a task first
    client.post(
        "/api/tasks",
        json={"title": "Task 1"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # List tasks
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) >= 1


def test_update_task(auth_token):
    """Test updating a task"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "Original Title"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    task_id = create_response.json()["data"]["id"]

    # Update task
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Title", "description": "Updated Description"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == "Updated Title"


def test_delete_task(auth_token):
    """Test deleting a task"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "To Delete"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    task_id = create_response.json()["data"]["id"]

    # Delete task
    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204


def test_toggle_task_status(auth_token):
    """Test toggling task completion status"""
    # Create task
    create_response = client.post(
        "/api/tasks",
        json={"title": "To Complete"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    task_id = create_response.json()["data"]["id"]

    # Mark as complete
    response = client.patch(
        f"/api/tasks/{task_id}/status",
        json={"completed": True},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["completed"] is True
