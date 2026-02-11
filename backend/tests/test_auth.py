import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_signup_success():
    """Test successful user signup"""
    response = client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "token" in data["data"]
    assert data["data"]["user"]["email"] == "test@example.com"


def test_signup_duplicate_email():
    """Test signup with duplicate email"""
    # First signup
    client.post(
        "/api/auth/signup",
        json={"email": "duplicate@example.com", "password": "testpass123"}
    )
    # Second signup with same email
    response = client.post(
        "/api/auth/signup",
        json={"email": "duplicate@example.com", "password": "testpass123"}
    )
    assert response.status_code == 400


def test_signup_invalid_email():
    """Test signup with invalid email format"""
    response = client.post(
        "/api/auth/signup",
        json={"email": "invalid-email", "password": "testpass123"}
    )
    assert response.status_code == 400


def test_signup_short_password():
    """Test signup with password less than 8 characters"""
    response = client.post(
        "/api/auth/signup",
        json={"email": "test2@example.com", "password": "short"}
    )
    assert response.status_code == 400


def test_signin_success():
    """Test successful user signin"""
    # First create user
    client.post(
        "/api/auth/signup",
        json={"email": "signin@example.com", "password": "testpass123"}
    )
    # Then sign in
    response = client.post(
        "/api/auth/signin",
        json={"email": "signin@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "token" in data["data"]


def test_signin_invalid_credentials():
    """Test signin with invalid credentials"""
    response = client.post(
        "/api/auth/signin",
        json={"email": "nonexistent@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_signout():
    """Test signout endpoint"""
    response = client.post("/api/auth/signout")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
