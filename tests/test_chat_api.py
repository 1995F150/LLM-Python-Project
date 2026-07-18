from fastapi.testclient import TestClient

from app import app
from engine.inference import InferenceResult

client = TestClient(app)
HEADERS = {"X-API-Key": "test-engine-key"}


def test_chat_contract_and_root_alias(monkeypatch):
    def fake_response(*args, **kwargs):
        return InferenceResult("Working response", "test-model", 7, 12)

    monkeypatch.setattr("api.chat.get_agent_response", fake_response)
    payload = {
        "message": "hey",
        "system_prompt": "Supabase context",
        "conversation_history": [],
        "user_id": None,
    }
    for path in ("/chat", "/chat-with-ai", "/api/chat"):
        response = client.post(path, headers=HEADERS, json=payload)
        assert response.status_code == 200
        assert response.json()["response"] == "Working response"
        assert response.json()["memories_used"] == 7


def test_chat_requires_api_key():
    response = client.post("/chat", json={"message": "hey"})
    assert response.status_code == 401


def test_chat_rejects_empty_message():
    response = client.post("/chat", headers=HEADERS, json={"message": ""})
    assert response.status_code == 422
