
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def find_spring():
    rag = RagService()
    # Search specifically for the Spring semester header likely to be in the next chunk
    query = "Vår 2026"
    print(f"--- Searching for: '{query}' ---")
    
    chunks = await rag.search_similar_chunks(query, limit=50, threshold=0.1)
    
    found = False
    for c in chunks:
        url = c.get('url', '')
        if "aarsstudium-i-logistikk" in url:
            print(f"\n[FOUND CHUNK] Score: {c.get('score', 0)}")
            print(f"URL: {url}")
            print(f"Content Preview: {c.get('content', '')[:200]}...")
            found = True
            
    if not found:
        print("No 'Vår 2026' chunk found for 'aarsstudium-i-logistikk'.")

if __name__ == "__main__":
    asyncio.run(find_spring())
