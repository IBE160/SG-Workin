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
    type: str = "answer" # answer | clarification

class ChatResponse(BaseModel):
    status: str
    data: ChatResponseData
