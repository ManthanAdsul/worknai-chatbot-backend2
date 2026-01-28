from pydantic import BaseModel
from typing import Optional, List

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    session_id: str
    detected_language: str


class UploadPDFRequest(BaseModel):
    file_name: str
    
class StatusResponse(BaseModel):
    status: str
    message: str