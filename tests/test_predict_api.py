from fastapi.testclient import TestClient
from httpx import Response

from src.main import app


client: TestClient = TestClient(app)


def test_predict() -> None:
    URL: str = "http://0.0.0.0:8000/api/v1/predict"
    X_QUERY: str = "?x=100.0"
    Y_QUERY: str = "&y=20.0"
    HEADERS: dict[str, str] = {
        "Content-Type": "application/json",
    }

    response: Response = client.get(
        url=URL + X_QUERY + Y_QUERY,
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {
        "model": "simple_predictor",
        "prediction": 2000.0,
    }


def test_predict_bad_data() -> None:
    URL: str = "http://0.0.0.0:8000/api/v1/predict"
    BAD_X_QUERY: str = "?x=100.0"
    BAD_Y_QUERY: str = "&y=cnn"
    HEADERS: dict[str, str] = {
        "Content-Type": "application/json",
    }

    response: Response = client.get(
        url=URL + BAD_X_QUERY + BAD_Y_QUERY,
        headers=HEADERS,
    )

    assert response.status_code == 422
