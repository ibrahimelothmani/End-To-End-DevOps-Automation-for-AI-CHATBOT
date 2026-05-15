import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Gemini AI Chatbot")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = None
if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)
else:
    print("WARNING: GOOGLE_API_KEY not found in environment variables")

class ChatRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/chat/")
def chat_with_bot(request: ChatRequest):
    if not client:
        return {"error": "API Key not configured"}
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=request.user_input
        )
        return {"bot_response": response.text}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)