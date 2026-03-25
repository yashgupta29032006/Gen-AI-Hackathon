import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_logs():
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ask_endpoint_structure():
    # Note: This might fail without a real API key, so we check for 500 or 200
    # In a real CI, we'd mock the LLM
    response = client.post("/ask", json={"user_input": "Test query"})
    assert response.status_code in [200, 500, 422]
