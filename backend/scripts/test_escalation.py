
import asyncio
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from backend.routers.chat import chat, get_rag_service
from backend.schemas.chat import ChatRequest
from backend.services.rag import RagService
from unittest.mock import MagicMock, AsyncMock

async def test_escalation():
    # Mock RagService
    mock_rag_service = MagicMock(spec=RagService)
    # Mock search_similar_chunks to return empty list (simulating no relevant info)
    mock_rag_service.search_similar_chunks = AsyncMock(return_value=[])
    # Mock detect_ambiguity to return not ambiguous
    mock_rag_service.detect_ambiguity = MagicMock(return_value={"is_ambiguous": False})
    
    # Mock contextualize_query to return query as is
    mock_rag_service.contextualize_query = MagicMock(side_effect=lambda q, h: q)

    request = ChatRequest(message="What is the airspeed velocity of an unladen swallow?")
    
    print("Testing escalation logic...")
    response = await chat(request, rag_service=mock_rag_service)
    
    print(f"Status: {response.status}")
    print(f"Type: {response.data.type}")
    print(f"Response Text: {response.data.response}")
    print(f"Escalation Link: {response.data.escalation_link}")
    
    if response.data.type == "escalation" and response.data.escalation_link is not None:
        print("\nSUCCESS: Escalation triggered correctly.")
    else:
        print("\nFAILURE: Escalation NOT triggered.")

if __name__ == "__main__":
    asyncio.run(test_escalation())
