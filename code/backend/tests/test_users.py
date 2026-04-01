"""User API endpoint tests."""

from app.models.models import User
from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "password": "SecurePass123!",
    }
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "newuser@example.com"
    assert "hashed_password" not in data


def test_create_duplicate_user(client: TestClient, test_user: User):
    payload = {
        "email": test_user.email,
        "password": "AnotherPass123!",
    }
    r = client.post("/users/", json=payload)
    assert r.status_code == 400
    assert "already registered" in r.json()["detail"]


def test_login(client: TestClient, test_user: User):
    r = client.post(
        "/token",
        data={"username": test_user.email, "password": "TestPass123!"},
    )
    assert r.status_code == 200
    assert "access_token" in r.json()
    assert r.json()["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user: User):
    r = client.post(
        "/token",
        data={"username": test_user.email, "password": "wrongpassword"},
    )
    assert r.status_code == 401


def test_get_me(client: TestClient, auth_headers: dict):
    r = client.get("/users/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "test@quantumnest.com"


def test_get_user_by_id(client: TestClient, auth_headers: dict, test_user: User):
    r = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["id"] == test_user.id


def test_get_nonexistent_user(client: TestClient, auth_headers: dict):
    r = client.get("/users/999999", headers=auth_headers)
    assert r.status_code == 404


def test_update_user(client: TestClient, auth_headers: dict, test_user: User):
    r = client.put(
        f"/users/{test_user.id}",
        json={"first_name": "Updated"},
        headers=auth_headers,
    )
    assert r.status_code == 200
    assert r.json()["first_name"] == "Updated"


def test_unauthenticated_access(client: TestClient):
    r = client.get("/users/me")
    assert r.status_code == 401
