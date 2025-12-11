from fastapi import APIRouter, Depends, HTTPException, status
from backend.services.rag import RagService
from backend.schemas.chat import ChatRequest, ChatResponse, ChatResponseData

router = APIRouter()

def get_rag_service():
    return RagService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, rag_service: RagService = Depends(get_rag_service)):
    """
    Handle chat messages using RAG pipeline with interactive guidance.
    """
    try:
        # 0. Contextualize query if history exists
        current_query = request.message
        if request.history:
            current_query = rag_service.contextualize_query(request.message, request.history)

        # 1. Check for ambiguity (Interactive Guidance)
        ambiguity_result = rag_service.detect_ambiguity(current_query)
        
        if ambiguity_result.get("is_ambiguous"):
            return ChatResponse(
                status="success",
                data=ChatResponseData(
                    response=ambiguity_result.get("clarifying_question", "Could you allow me to clarify?"),
                    type="clarification"
                )
            )

        # 2. Retrieve context (if specific)
        chunks = await rag_service.search_similar_chunks(current_query)
        
        # 3. Generate answer
        # We pass the rewritten query so the answer generation also benefits from the resolved context
        response_text = rag_service.generate_answer(current_query, chunks)

        return ChatResponse(
            status="success",
            data=ChatResponseData(
                response=response_text,
                type="answer"
            )
        )
    except Exception as e:
        # Log the error here
        print(f"Error in chat endpoint: {e}")
        return ChatResponse(
            status="error",
            data=ChatResponseData(
                response="I apologize, but I'm currently unable to access my knowledge base. Please try again later."
            )
        )
