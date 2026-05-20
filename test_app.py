from fastapi.testclient import TestClient
from api.index import app
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_state():
    client.delete("/api/reset")
    yield

def test_frontend_serves():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Gemini Clone" in response.text

def test_read_empty_state():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json() == {"data": {}}

def test_write_and_llm_processing():
    response = client.post("/api/data", json={"text": "Reply with exactly the word: 'Banana'"})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Success"
    assert data["id"] == 1
    assert "data" in data
    assert data["data"]["user"] == "Reply with exactly the word: 'Banana'"
    assert "banana" in data["data"]["ai"].lower()

def test_write_invalid_payload():
    response = client.post("/api/data", json={"wrong_key": "Hello"})
    assert response.status_code == 422

def test_delete_existing_item():
    post_res = client.post("/api/data", json={"text": "Temporary message for deletion."})
    item_id = post_res.json()["id"]
    
    del_res = client.delete(f"/api/data/{item_id}")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == f"Item {item_id} deleted."
    
    get_res = client.get("/api/data")
    assert str(item_id) not in get_res.json()["data"]

def test_delete_non_existent_item():
    response = client.delete("/api/data/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_reset_data():
    client.post("/api/data", json={"text": "Message 1"})
    client.post("/api/data", json={"text": "Message 2"})
    
    reset_res = client.delete("/api/reset")
    assert reset_res.status_code == 200
    assert reset_res.json()["message"] == "Chat memory reset."
    
    get_res = client.get("/api/data")
    assert get_res.json()["data"] == {}
