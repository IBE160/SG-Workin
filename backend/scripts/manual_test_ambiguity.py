import asyncio
import sys
import os

# Add backend to path
# Add project root to path (SG-Workin)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from backend.services.rag import RagService


async def test_ambiguity():
    rag = RagService()
    
    queries = [
        "Bachelor in Logistics", # Specific
        "business", # Ambiguous
        "Tell me about studies", # Ambiguous
        "Who is the rector?", # Specific
    ]
    
    print("🤖 Testing Ambiguity Detection...\n")
    
    for q in queries:
        print(f"Query: '{q}'")
        result = rag.detect_ambiguity(q)
        print(f"Result: {result}\n")

if __name__ == "__main__":
    asyncio.run(test_ambiguity())
