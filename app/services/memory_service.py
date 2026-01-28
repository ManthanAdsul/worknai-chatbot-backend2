from typing import Dict, List
import json
import os
from datetime import datetime
from app.config import settings

class MemoryService:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.log_dir = "./data/chat_logs"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to session history."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        self.sessions[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last N messages
        max_history = settings.MAX_CONVERSATION_HISTORY * 2
        if len(self.sessions[session_id]) > max_history:
            self.sessions[session_id] = self.sessions[session_id][-max_history:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session."""
        return self.sessions.get(session_id, [])
    
    def format_history_for_prompt(self, session_id: str) -> str:
        """Format history as a readable string for the prompt."""
        history = self.get_history(session_id)
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history[-10:]:
            role = "Student" if msg["role"] == "user" else "Mentor"
            formatted.append(f"{role}: {msg['content']}")
        
        return "\n".join(formatted)
    
    def save_session(self, session_id: str):
        """Save session to file for logging."""
        if session_id in self.sessions:
            file_path = os.path.join(self.log_dir, f"{session_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.sessions[session_id], f, ensure_ascii=False, indent=2)

# Global instance
memory_service = MemoryService()