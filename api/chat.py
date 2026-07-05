# API endpoint for chat functionality
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(message: str):
    """Handles chat messages via the API."""
    return {"message": "Chat endpoint received: " + message}
