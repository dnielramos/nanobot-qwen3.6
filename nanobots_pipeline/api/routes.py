from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.orchestrator import orchestrator
from memory.short_term import short_term_memory
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    prompt: str

class ChatResponse(BaseModel):
    session_id: str
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main entry point for UI interactions.
    If no session_id is provided, a new session is created.
    """
    try:
        session_id = request.session_id or short_term_memory.create_session()
        reply = await orchestrator.process_request(session_id, request.prompt)
        return ChatResponse(session_id=session_id, reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    """Clears the short-term memory session."""
    short_term_memory.clear_session(session_id)
    return {"message": f"Session {session_id} cleared."}
