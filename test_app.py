from fastapi.testclient import TestClient
from api.index import app
import pytest

client = TestClient(app)

# This fixture runs before every single test to ensure a clean database.
# It prevents tests from failing due to leftover data from a previous test.
@pytest.fixture(autouse=True)
def reset_state():
    client.delete("/api/reset")
    yield

def test_frontend_serves():
    """Test if the HTML frontend is successfully delivered."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Gemini Clone" in response.text

def test_read_empty_state():
    """Test reading data when the database is empty."""
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json() == {"data": {}}

def test_write_and_llm_processing():
    """Test writing data, connecting to OpenRouter, and saving the response."""
    # We use a very specific prompt to guarantee a predictable, fast test response
    response = client.post("/api/data", json={"text": "Reply with exactly the word: 'Banana'"})
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Success"
    assert data["id"] == 1
    assert "data" in data
    assert data["data"]["user"] == "Reply with exactly the word: 'Banana'"
    assert "banana" in data["data"]["ai"].lower()

def test_write_invalid_payload():
    """Test that the API rejects bad data formats (Validation Error)."""
    response = client.post("/api/data", json={"wrong_key": "Hello"})
    assert response.status_code == 422 # HTTP 422: Unprocessable Entity

def test_delete_existing_item():
    """Test creating an item and then successfully deleting it."""
    # 1. Create the item
    post_res = client.post("/api/data", json={"text": "Temporary message for deletion."})
    item_id = post_res.json()["id"]
    
    # 2. Delete the item
    del_res = client.delete(f"/api/data/{item_id}")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == f"Item {item_id} deleted."
    
    # 3. Verify it is actually gone
    get_res = client.get("/api/data")
    assert str(item_id) not in get_res.json()["data"]

def test_delete_non_existent_item():
    """Test that deleting a fake ID returns a proper 404 error."""
    response = client.delete("/api/data/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_reset_data():
    """Test that the memory wipe feature works perfectly."""
    # 1. Populate with multiple messages
    client.post("/api/data", json={"text": "Message 1"})
    client.post("/api/data", json={"text": "Message 2"})
    
    # 2. Trigger the reset
    reset_res = client.delete("/api/reset")
    assert reset_res.status_code == 200
    assert reset_res.json()["message"] == "Chat memory reset."
    
    # 3. Verify complete wipe
    get_res = client.get("/api/data")
    assert get_res.json()["data"] == {}
