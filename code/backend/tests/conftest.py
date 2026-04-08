"""
Shared pytest fixtures for QuantumNest tests.

Uses an in-memory SQLite database so no external services are required.
"""

import logging
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Set env vars BEFORE importing app modules so Settings picks them up
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-at-least-32-chars!!")
os.environ.setdefault("API_SECRET_KEY", "test-api-secret-key-min-32-chars-here!!")
os.environ.setdefault("ENVIRONMENT", "development")

from app.db.database import get_db  # noqa: E402  (env must be set first)
from app.main import app  # noqa: E402
from app.models.models import Base, User  # noqa: E402

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


# ── In-memory test database ───────────────────────────────────────────────────

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Yield a transactional DB session that rolls back after each test."""
    connection = TEST_ENGINE.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """FastAPI TestClient with the real DB overridden by the test session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Common test data fixtures ─────────────────────────────────────────────────


@pytest.fixture()
def test_user(db_session: Session) -> User:
    """Create and return a basic test user."""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = User(
        email="test@quantumnest.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=pwd_context.hash("TestPass123!"),
        role="user",
        tier="basic",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def admin_user(db_session: Session) -> User:
    """Create and return an admin test user."""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = User(
        email="admin@quantumnest.com",
        username="adminuser",
        first_name="Admin",
        last_name="User",
        hashed_password=pwd_context.hash("AdminPass123!"),
        role="admin",
        tier="enterprise",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def auth_headers(client: TestClient, test_user: User) -> dict:
    """Return Authorization headers for the test user."""
    response = client.post(
        "/token",
        data={"username": test_user.email, "password": "TestPass123!"},
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def admin_headers(client: TestClient, admin_user: User) -> dict:
    """Return Authorization headers for the admin user."""
    response = client.post(
        "/token",
        data={"username": admin_user.email, "password": "AdminPass123!"},
    )
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ── Authentication system fixtures ───────────────────────────────────────────


@pytest.fixture()
def mock_redis():
    """Return a MagicMock that mimics a Redis client."""
    from unittest.mock import MagicMock

    redis_mock = MagicMock()
    redis_mock.get.return_value = None
    redis_mock.setex.return_value = True
    redis_mock.incr.return_value = 1
    redis_mock.delete.return_value = 1
    return redis_mock


@pytest.fixture()
def auth_system(db_session, mock_redis):
    """Return an AdvancedAuthenticationSystem wired to test DB and mock Redis."""
    from unittest.mock import patch

    from app.auth.authentication import AdvancedAuthenticationSystem

    with patch("app.auth.authentication.redis.Redis", return_value=mock_redis):
        system = AdvancedAuthenticationSystem(db_session)
    # Replace the real redis client with the mock so tests can inspect calls
    system.redis_client = mock_redis
    return system
