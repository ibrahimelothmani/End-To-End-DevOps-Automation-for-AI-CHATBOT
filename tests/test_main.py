import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

def test_read_root():
    # The root returns a FileResponse (index.html)
    response = client.get("/")
    assert response.status_code == 200
    # We can check if it's an HTML response
    assert "text/html" in response.headers["content-type"]

def test_chat():
    with patch('main.client') as mock_genai_client:
        mock_response = MagicMock()
        mock_response.text = "Hello, I am Gemini!"
        mock_genai_client.models.generate_content.return_value = mock_response
        
        response = client.post("/chat/", json={"user_input": "hi"})
        assert response.status_code == 200
        assert response.json() == {"bot_response": "Hello, I am Gemini!"}

def test_chat_no_key():
    with patch('main.client', None):
        response = client.post("/chat/", json={"user_input": "hi"})
        assert response.status_code == 200
        assert response.json() == {"error": "API Key not configured"}
