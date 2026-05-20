from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)

def test_read_empty():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json() == {"data": {}}

def test_write_and_llm_processing():
    response = client.post("/api/data", json={"text": "Say the word 'Banana' and nothing else."})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "Success"
    
    # Check that both the user prompt and the AI response were saved correctly
    assert json_data["data"]["user"] == "Say the word 'Banana' and nothing else."
    
    ai_response = json_data["data"]["ai"].lower()
    assert "banana" in ai_response

def test_delete_function():
    # 1. Write an item
    post_res = client.post("/api/data", json={"text": "Delete me."})
    item_id = post_res.json()["id"]
    
    # 2. Delete the item
    del_res = client.delete(f"/api/data/{item_id}")
    assert del_res.status_code == 200
    
    # 3. Verify it is gone
    get_res = client.get("/api/data")
    assert str(item_id) not in get_res.json()["data"]

def test_reset_data():
    # 1. Write an item to ensure the DB isn't empty
    client.post("/api/data", json={"text": "Populate the database."})
    
    # 2. Call the reset endpoint
    reset_res = client.delete("/api/reset")
    assert reset_res.status_code == 200
    assert reset_res.json()["message"] == "Chat memory reset."
    
    # 3. Verify the database is empty
    get_res = client.get("/api/data")
    assert get_res.json()["data"] == {}
