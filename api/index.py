import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
from dotenv import load_dotenv

# Load the .env file for local development
load_dotenv()

app = FastAPI()

# Simple in-memory database for our Read/Write/Delete requirements
db: Dict[int, str] = {}
current_id = 1

# Retrieve the API key from environment variables
API_KEY = os.getenv("OpenRouter-API-Keys")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class TextItem(BaseModel):
    text: str

# --- Local Testing Route ---
@app.get("/")
def serve_frontend():
    """Serves the HTML frontend when testing locally."""
    return FileResponse("public/index.html")
# ---------------------------

@app.get("/api/data")
def read_data():
    """READ: Get all processed items"""
    return {"data": db}

@app.post("/api/data")
async def write_data(item: TextItem):
    """WRITE: Send text to OpenRouter LLM and save response"""
    global current_id
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://github.com/yourusername/devops-llm-app", # Required by OpenRouter
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "google/gemini-3.5-flash",
        "messages": [{"role": "user", "content": item.text}]
    }

    try:
        # Call OpenRouter API asynchronously
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            llm_response = data["choices"][0]["message"]["content"]
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    # Save to database
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
