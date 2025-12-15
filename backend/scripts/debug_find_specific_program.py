
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def find_program():
    rag = RagService()
    query = "Årsstudium i logistikk"
    print(f"--- Searching specifically for: '{query}' ---")
    
    # Very low threshold to find ANYTHING related
    chunks = await rag.search_similar_chunks(query, limit=20, threshold=0.1)
    
    print(f"\nFound {len(chunks)} chunks:")
    for i, c in enumerate(chunks):
        title = c.get('title', 'No Title')
        url = c.get('url', 'No URL')
        score = c.get('score', 0)
        content = c.get('content', '')[:100].replace('\n', ' ')
        
        if "årsstudium" in content.lower() or "årsstudium" in title.lower() or "logistikk" in url.lower():
             print(f"[{i+1}] Score: {score:.4f} | {url}")
             print(f"    Content: {content}...")

if __name__ == "__main__":
    asyncio.run(find_program())
