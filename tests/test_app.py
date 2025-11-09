from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_index_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bible Coach" in response.text


def test_chat_endpoint_intro():
    response = client.post("/api/chat", json={"messages": []})
    assert response.status_code == 200
    payload = response.json()
    assert "reply" in payload
    assert "Bible Coach" in payload["reply"]


def test_chat_endpoint_observation():
    conversation = {"messages": [{"role": "user", "content": "John 3:16"}]}
    response = client.post("/api/chat", json=conversation)
    assert response.status_code == 200
    payload = response.json()
    assert "Observation focus" in payload["reply"]
