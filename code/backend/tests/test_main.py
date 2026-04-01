"""Basic smoke tests for core endpoints."""

from fastapi.testclient import TestClient


def test_root(client: TestClient):
    r = client.get("/")
    assert r.status_code == 200
    assert "QuantumNest" in r.json()["message"]


def test_health(client: TestClient):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_docs_available(client: TestClient):
    r = client.get("/docs")
    assert r.status_code == 200


def test_openapi_schema(client: TestClient):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    assert schema["info"]["title"] == "QuantumNest Capital API"
