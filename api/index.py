import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

db: Dict[int, Dict[str, str]] = {}
current_id = 1

API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OpenRouter-API-Keys")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class TextItem(BaseModel):
    text: str

@app.get("/")
def serve_frontend():
    # Calculate the absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "public", "index.html")
    
    # If it exists (like on your local machine), serve it via Python
    if os.path.exists(file_path):
        return FileResponse(file_path)
        
    # If it doesn't exist (like on Vercel), return a safe API message
    # Vercel's routing should intercept the HTML request before it ever reaches this anyway!
    return {"message": "API is active. Frontend is handled by Vercel CDN."}

@app.get("/api/data")
def read_data():
    return {"data": db}

@app.post("/api/data")
async def write_data(item: TextItem):
    global current_id
    
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key not configured")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://github.com/yourusername/devops-llm-app",
        "Content-Type": "application/json"
    }
    
    messages = [{"role": "system", "content": "You are Gemini, a helpful AI."}]
    
    for key in sorted(db.keys()):
        messages.append({"role": "user", "content": db[key]["user"]})
        messages.append({"role": "assistant", "content": db[key]["ai"]})
        
    messages.append({"role": "user", "content": item.text})
    
    payload = {
        "model": "google/gemini-3.5-flash",
        "messages": messages
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            llm_response = data["choices"][0]["message"]["content"]
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    db[current_id] = {"user": item.text, "ai": llm_response}
    inserted_id = current_id
    current_id += 1
    
    return {"message": "Success", "id": inserted_id, "data": db[inserted_id]}

@app.delete("/api/data/{item_id}")
def delete_data(item_id: int):
    if item_id in db:
        del db[item_id]
        return {"message": f"Item {item_id} deleted."}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/reset")
def reset_data():
    global db, current_id
    db.clear()
    current_id = 1
    return {"message": "Chat memory reset."}
