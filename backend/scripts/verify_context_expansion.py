
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def verify_neighbors():
    rag = RagService()
    # Use the precise query that retrieves Chunk 0 (Autumn)
    query = "hvilke fag inngår i årsstudium logistikk?"
    
    print(f"--- Verifying Neighbor Retrieval for: '{query}' ---")
    
    # We expect 'search_similar_chunks' to now internally fetch neighbors
    chunks = await rag.search_similar_chunks(query, limit=50, threshold=0.1)
    
    print(f"\nTotal Chunks Retrieved: {len(chunks)}")
    
    neighbor_found = False
    autumn_found = False
    
    for c in chunks:
        content = c.get('content', '')
        is_neighbor = c.get('is_neighbor', False)
        
        if "Prinsipper i verdikjedeledelse" in content:
            autumn_found = True
            print(f"Found Autumn Chunk (Original). ID: {c.get('id')}")
            
        if "SCM210" in content and "Vår" in content: # This is in the neighbor
            neighbor_found = True
            print(f"Found Spring Chunk (Neighbor). ID: {c.get('id')} | IsNeighbor: {is_neighbor}")
            
            if is_neighbor:
                print("SUCCESS: Chunk was fetched via neighbor expansion!")
            else:
                print("NOTE: Chunk was fetched normally (maybe limit increase helped?)")

    if autumn_found and neighbor_found:
        print("\nVERIFICATION PASSED: Both semesters available in context.")
    else:
        print("\nVERIFICATION FAILED: Missing semester.")

if __name__ == "__main__":
    asyncio.run(verify_neighbors())
