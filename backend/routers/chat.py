from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.rag import RagService

router = APIRouter()
rag_service = RagService()

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
    Handle chat messages using RAG pipeline.
    """
    # 1. Retrieve context
    chunks = await rag_service.search_similar_chunks(request.message)
    
    # 2. Generate answer
    response_text = rag_service.generate_answer(request.message, chunks)

    return ChatResponse(
        status="success",
        data=ChatResponseData(
            response=response_text
        )
    )
