
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def inspect_chunk():
    rag = RagService()
    # Search for the specific URL to find the chunk ID or just filter by URL
    target_url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/oppbygging/"
    
    print(f"--- Inspecting Chunk for URL: {target_url} ---")
    
    # Use the USER'S query which we know works (Rank 22)
    chunks = await rag.search_similar_chunks("hvilke fag inngår i årsstudium logistikk?", limit=50, threshold=0.1)
    
    found = False
    for c in chunks:
        if "oppbygging" in c.get('url', '') and "aarsstudium-i-logistikk" in c.get('url', ''):
            print(f"\n[FOUND CHUNK] Score: {c.get('score')}")
            print(f"Content Length: {len(c.get('content', ''))}")
            print("--- BEGIN CONTENT ---")
            print(c.get('content', ''))
            print("--- END CONTENT ---")
            found = True
            break
            
    if not found:
        print("Chunk not found via search.")

if __name__ == "__main__":
    asyncio.run(inspect_chunk())
