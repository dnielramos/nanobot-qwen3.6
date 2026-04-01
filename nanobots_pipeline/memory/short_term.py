import uuid
from typing import Dict, List

class ShortTermMemory:
    """Session-based memory for short-term conversational context."""
    def __init__(self):
        self.sessions: Dict[str, List[dict]] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        return session_id

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append({"role": role, "content": content})

    def get_context(self, session_id: str) -> List[dict]:
        return self.sessions.get(session_id, [])

    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

short_term_memory = ShortTermMemory()
