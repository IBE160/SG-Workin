from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponseData(BaseModel):
    response: str

class ChatResponse(BaseModel):
    status: str
    data: ChatResponseData

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat messages.
    Returns a hardcoded 'Hello World' response for now.
    """
    return ChatResponse(
        status="success",
        data=ChatResponseData(
            response="Hello! I am the university chatbot. How can I help you today?"
        )
    )
