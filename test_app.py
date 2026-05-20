from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_read_empty():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json() == {"data": {}}

def test_write_and_llm_processing():
    response = client.post("/api/data", json={"text": "hello test"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Success"
    assert "hello test" in data["text"]
    assert "🤖 AI Summary" in data["text"]

def test_delete_function():
    # 1. Write an item
    post_res = client.post("/api/data", json={"text": "delete me"})
    item_id = post_res.json()["id"]
    
    # 2. Delete the item
    del_res = client.delete(f"/api/data/{item_id}")
    assert del_res.status_code == 200
    
    # 3. Verify it is gone
    get_res = client.get("/api/data")
    assert str(item_id) not in get_res.json()["data"]
