"""AI API endpoint tests."""

from typing import Any
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient


class MockAsyncResult:
    def __init__(self, id: Any, status: Any = "SUCCESS", result: Any = None) -> None:
        self.id = id
        self._status = status
        self._result = result

    @property
    def status(self) -> Any:
        return self._status

    def ready(self) -> Any:
        return self._status in ["SUCCESS", "FAILURE"]

    def successful(self) -> Any:
        return self._status == "SUCCESS"

    @property
    def result(self) -> Any:
        return self._result


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_get_ai_models(client: TestClient, auth_headers: dict) -> None:
    """Test listing AI models returns a list."""
    response = client.get("/ai/models/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_ai_model_not_found(client: TestClient, auth_headers: dict) -> None:
    """Test fetching non-existent AI model returns 404."""
    response = client.get("/ai/models/999999", headers=auth_headers)
    assert response.status_code == 404


def test_get_ai_predictions(client: TestClient, auth_headers: dict) -> None:
    """Test listing AI predictions returns a list."""
    response = client.get("/ai/predictions/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@patch("app.api.ai.predict_asset_price")
def test_predict_asset_price(
    mock_predict: Any, client: TestClient, auth_headers: dict
) -> None:
    """Test asset price prediction endpoint."""
    task_id = "test-task-id"
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_predict.delay.return_value = mock_task

    response = client.post("/ai/predict/asset/AAPL", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "PENDING"
    assert "check_status_endpoint" in data
    mock_predict.delay.assert_called_once_with("AAPL", 5, "lstm")


@patch("app.api.ai.AsyncResult")
def test_get_task_status(
    mock_async_result: Any, client: TestClient, auth_headers: dict
) -> None:
    """Test task status endpoint."""
    task_id = "test-task-id"
    mock_result = {
        "asset_symbol": "AAPL",
        "model_type": "lstm",
        "predictions": [{"date": "2025-05-20", "predicted_price": 200.0}],
    }
    mock_async_result.return_value = MockAsyncResult(task_id, "SUCCESS", mock_result)

    response = client.get(f"/ai/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "SUCCESS"
    assert data["result"] == mock_result


@patch("app.api.ai.analyze_sentiment")
def test_analyze_sentiment(
    mock_analyze: Any, client: TestClient, auth_headers: dict
) -> None:
    """Test sentiment analysis endpoint."""
    task_id = "test-task-id"
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_analyze.delay.return_value = mock_task

    response = client.post("/ai/sentiment/asset/AAPL", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "PENDING"
    assert "check_status_endpoint" in data
    mock_analyze.delay.assert_called_once_with("AAPL", None)


@patch("app.api.ai.generate_market_recommendations")
def test_market_recommendations(
    mock_generate: Any, client: TestClient, auth_headers: dict
) -> None:
    """Test market recommendations endpoint."""
    task_id = "test-task-id"
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_generate.delay.return_value = mock_task

    response = client.post("/ai/recommendations/market", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == task_id
    assert data["status"] == "PENDING"
    assert "check_status_endpoint" in data
    mock_generate.delay.assert_called_once()


def test_deprecated_portfolio_recommendations(
    client: TestClient, auth_headers: dict
) -> None:
    """Test deprecated GET portfolio recommendations endpoint still responds."""
    response = client.get("/ai/recommendations/portfolio/999999", headers=auth_headers)
    # 404 is expected since portfolio doesn't exist; the point is it routes correctly
    assert response.status_code in (200, 404)


def test_deprecated_market_recommendations(
    client: TestClient, auth_headers: dict
) -> None:
    """Test deprecated GET market recommendations endpoint still responds."""
    response = client.get("/ai/recommendations/market", headers=auth_headers)
    assert response.status_code == 200


def test_deprecated_sentiment(client: TestClient, auth_headers: dict) -> None:
    """Test deprecated GET sentiment endpoint still responds."""
    response = client.get("/ai/sentiment/asset/AAPL", headers=auth_headers)
    assert response.status_code == 200


def test_deprecated_risk(client: TestClient, auth_headers: dict) -> None:
    """Test deprecated GET risk endpoint still responds."""
    response = client.get("/ai/risk/portfolio/999999", headers=auth_headers)
    # 404 expected since portfolio doesn't exist
    assert response.status_code in (200, 404)


def test_ai_unauthenticated(client: TestClient) -> None:
    """Test AI endpoints require authentication."""
    r = client.get("/ai/models/")
    assert r.status_code == 401
