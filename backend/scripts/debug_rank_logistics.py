
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def check_rank():
    rag = RagService()
    query = "Hei, hvilke årsstudier tilbyr dere?"
    
    print(f"--- Checking Rank for 'Logistikk' in query: '{query}' ---")
    
    # High limit, low threshold to catch it
    chunks = await rag.search_similar_chunks(query, limit=100, threshold=0.1)
    
    print(f"Retrieved {len(chunks)} chunks total.")
    
    found = False
    for i, c in enumerate(chunks):
        title = c.get('title', 'No Title')
        url = c.get('url', '')
        content = c.get('content', '')
        
        # Look for the specific logistics one-year program
        if "aarsstudium-i-logistikk" in url or ("årsstudium" in content.lower() and "logistikk" in content.lower()):
            print(f"\n[RANK {i+1}] Score: {c.get('score', 'N/A')} | URL: {url}")
            print(f"Preview: {content[:100]}...")
            found = True
            
    if not found:
        print("\nNOT FOUND even in top 100 with threshold 0.1!")

if __name__ == "__main__":
    asyncio.run(check_rank())
