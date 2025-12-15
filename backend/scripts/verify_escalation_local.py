
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService
from backend.core.config import settings

# Configure logging to see if it retrieves chunks
logging.basicConfig(level=logging.INFO)

async def verify_local():
    rag = RagService()
    
    # Nonsense query
    query = "wabadubadubdub what is the meaning of life in mars?"
    print(f"Query: {query}")
    
    # 1. Inspect Prompt (Sanity Check)
    if "kontakt-oss" not in settings.RAG_SYSTEM_PROMPT:
        print("❌ FAIL: Config not updated with contact link!")
        return

    # 2. Generate Answer
    # logic from chat.py: search then generate
    chunks = await rag.search_similar_chunks(query, limit=5)
    print(f"Retrieved {len(chunks)} chunks.")
    
    response = rag.generate_answer(query, chunks)
    print(f"\n--- Response ---\n{response}\n----------------")
    
    if "himolde.no/kontakt-oss" in response:
        print("✅ PASS: Contact link found.")
    else:
        print("❌ FAIL: Contact link NOT found.")

if __name__ == "__main__":
    asyncio.run(verify_local())
