from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_get_frames():
    response = client.get("/frames/?depth_min=10&depth_max=100")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_frames_not_found():
    response = client.get("/frames/?depth_min=1000&depth_max=2000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No frames found in the specified range."}
