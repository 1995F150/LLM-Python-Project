from fastapi.testclient import TestClient

from app import app

client = TestClient(app)
HEADERS = {"X-API-Key": "test-engine-key"}


class FakeResponse:
    ok = True

    def raise_for_status(self):
        return None

    def json(self):
        return {"images": ["aGVsbG8="]}


def test_generate_image_contract(monkeypatch):
    monkeypatch.setattr("api.image._database_references", lambda *args: [])
    monkeypatch.setattr(
        "api.image.requests.post", lambda *args, **kwargs: FakeResponse()
    )
    response = client.post(
        "/image/generate", headers=HEADERS, json={"prompt": "a red barn"}
    )
    assert response.status_code == 200
    assert response.json()["image_url"].startswith("data:image/png;base64,")
    assert response.json()["references_used"] == 0


def test_analyze_requires_an_image():
    response = client.post("/image/analyze", headers=HEADERS, json={})
    assert response.status_code == 422
