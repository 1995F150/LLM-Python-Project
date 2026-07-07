import uuid
import time
import logging
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.auth import validate_api_key
from engine.agent import get_agent_response

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None

@router.post("/chat")
async def chat(request: ChatRequest, api_key: str = Depends(validate_api_key)):
    start_time = time.time()
    
    # Generate session ID and handle defaults
    session_id = str(uuid.uuid4())
    conversation_id = request.conversation_id or str(uuid.uuid4())
    user_id = request.user_id or "guest"

    # Get response from agent (returns tuple: (response_text, memories_count))
    response_text, memories_used = get_agent_response(
        request.message, 
        user_id=user_id, 
        conversation_id=conversation_id
    )
    
    latency_ms = int((time.time() - start_time) * 1000)

    # Logging requirements
    logger.info(f"Request Message: {request.message}")
    logger.info(f"User ID: {user_id}")
    logger.info(f"Conversation ID: {conversation_id}")
    logger.info(f"Memory Rows Used: {memories_used}")
    logger.info(f"Raw Ollama Response Length: {len(response_text)}")
    logger.info(f"Final Response Length: {len(response_text)}")
    logger.info(f"Response Field Returned: {response_text}")

    # Return strict output format
    return {
        "response": response_text,
        "session_id": session_id,
        "conversation_id": conversation_id,
        "memories_used": memories_used,
        "latency_ms": latency_ms
    }
