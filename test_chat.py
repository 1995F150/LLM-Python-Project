from fastapi.testclient import TestClient
from app import app
import pytest

client = TestClient(app)

def test_chat_with_ai_success():
    response = client.post("/chat-with-ai", json={
        "text": "Hello",
        "user_id": "test_user",
        "conversation_id": "conv_123"
    })
    assert response.status_code == 200
    assert "response" in response.json()

def test_chat_success():
    response = client.post("/chat", json={
        "message": "Hi there",
        "user_id": "test_user",
        "conversation_id": "conv_456"
    })
    assert response.status_code == 200
    assert "response" in response.json()

def test_missing_user_id():
    response = client.post("/chat", json={
        "message": "Hello"
    })
    assert response.status_code in [400, 422]

def test_missing_text_and_message():
    response = client.post("/chat", json={
        "user_id": "test_user"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Either 'text' or 'message' must be provided"
