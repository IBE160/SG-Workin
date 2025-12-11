
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.rag import RagService
from backend.schemas.chat import ChatMessage

async def test_history():
    rag = RagService()
    
    # Simulate history: User asked about "Bachelor in Logistics", Assistant answered.
    # Now user asks "What are the admission requirements?"
    # Without history, this is ambiguous/generic.
    # With history, it is specific ("Admission requirements for Bachelor in Logistics").
    
    history = [
        ChatMessage(role="user", content="Tell me about Bachelor in Logistics"),
        ChatMessage(role="assistant", content="We have a Bachelor in Logistics program...")
    ]
    
    query = "What are the admission requirements?"
    
    print(f"Query: '{query}'")
    print(f"History: {len(history)} items")
    
    # We expect the currently implemented service to IGNORE history, so it might treat it as ambiguous
    # or just search for generic "admission requirements".
    
    # Ideally, we want a method that takes history.
    # But current signatures don't support it.
    
    # This test confirms the contextualize_query works
    try:
        print(f"Original Query: '{query}'")
        
        # 1. Contextualize
        rewritten = rag.contextualize_query(query, history)
        print(f"Rewritten Query: '{rewritten}'")
        
        # 2. Check ambiguity on rewritten query
        result = rag.detect_ambiguity(rewritten)
        print(f"Result (ambiguity): {result}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_history())
