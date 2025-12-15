from pydantic import BaseModel
from typing import Literal, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []

class ChatResponseData(BaseModel):
    response: str
    sources: list[str] = [] # List of source URLs
    escalation_link: Optional[str] = None
    type: str = "answer" # answer | clarification | escalation

class ChatResponse(BaseModel):
    status: str
    data: ChatResponseData
