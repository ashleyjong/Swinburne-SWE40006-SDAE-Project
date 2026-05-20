from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Simple in-memory database for our Read/Write/Delete requirements
db: Dict[int, str] = {}
current_id = 1

class TextItem(BaseModel):
    text: str

@app.get("/api/data")
def read_data():
    """READ: Get all processed items"""
    return {"data": db}

@app.post("/api/data")
def write_data(item: TextItem):
    """WRITE: Process text through our 'LLM' and save it"""
    global current_id
    
    # Simulated LLM Processing (To guarantee reliable deployment without API key issues)
    llm_response = f"🤖 AI Summary: The user said '{item.text}'. This is a simulated LLM response."
    
    db[current_id] = llm_response
    inserted_id = current_id
    current_id += 1
    
    return {"message": "Success", "id": inserted_id, "text": llm_response}

@app.delete("/api/data/{item_id}")
def delete_data(item_id: int):
    """DELETE: Remove an item"""
    if item_id in db:
        del db[item_id]
        return {"message": f"Item {item_id} deleted."}
    raise HTTPException(status_code=404, detail="Item not found")
