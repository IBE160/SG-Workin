
import logging
import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_retrieval():
    print("Initializing RAG Service...")
    rag = RagService()
    
    query = "list all bachelor programs"
    print(f"\n--- Searching for: '{query}' ---")
    
    # We expect limit=20 now
    chunks = await rag.search_similar_chunks(query, limit=20)
    
    print(f"Found {len(chunks)} chunks.")
    
    # helper to print titles
    seen_titles = set()
    for c in chunks:
        title = c.get('metadata', {}).get('title', 'Unknown')
        if title not in seen_titles:
            print(f"- {title}")
            seen_titles.add(title)
            
    if len(chunks) > 5:
        print("\n✅ SUCCESS: Retrieval limit is > 5.")
    else:
        print("\n❌ FAILURE: Still retrieving few results. Check logic.")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
