from fastapi.testclient import TestClient
from src.main import app
import os


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    sha = os.getenv("SHA")
    assert response.json() == {"message": "Hello from commit " + sha}
