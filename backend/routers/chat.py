from fastapi import APIRouter, Depends, HTTPException, status
from backend.services.rag import RagService
from backend.schemas.chat import ChatRequest, ChatResponse, ChatResponseData
from backend.core.config import settings

import logging

logger = logging.getLogger(__name__)

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

        # 2. Retrieve context (Dynamic Limit)
        # Verify if user wants a comprehensive list (Global discovery)
        # We removed "hvilke fag"/"which courses" as they often appear in specific questions (e.g. "which subjects are in IT?")
        # Re-adding specific phrasing that implies a full list is needed to ensure Structure chunks are retrieved.
        list_keywords = [
            "list all", "list alle", "oversikt", 
            "hvilke programmer har dere", "hvilke studier har dere", 
            "what programs do you have", "alle studier", "alle programmer",
            "hvilke fag", "hvilke emner", "which courses", "what courses", "course list", "fagliste",
            "årsstudier", "year studies", "bachelor", "master", "phd"
        ]
        is_list_query = any(kw in current_query.lower() for kw in list_keywords)
        
        # INCREASED LIMIT: Rank analysis showed "Årsstudium i logistikk" at Rank 51. 50 is too tight.
        limit = 100 if is_list_query else 30
        logger.info(f"Query: '{current_query}' | Is List: {is_list_query} | Limit: {limit}")

        chunks = await rag_service.search_similar_chunks(current_query, limit=limit)
        
        # If no chunks, we still call generate_answer to handle greetings/chitchat
        
        # 3. Generate answer
        # We pass the rewritten query so the answer generation also benefits from the resolved context
        response_text = rag_service.generate_answer(current_query, chunks)
        sources = rag_service.extract_sources(chunks)

        return ChatResponse(
            status="success",
            data=ChatResponseData(
                response=response_text,
                sources=sources,
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
