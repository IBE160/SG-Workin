
import asyncio
import os
import sys
from dotenv import load_dotenv

# Ensure backend modules are found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load env vars
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env')))

from backend.services.rag import RagService

async def main():
    print("Initializing RagService...")
    try:
        rag = RagService()
        
        queries = ["hi", "Bachelor i logistikk"]
        
        for query in queries:
            print(f"\n--- Searching for: '{query}' ---")
            chunks = await rag.search_similar_chunks(query)
            
            print(f"Chunks found: {len(chunks)}")
            if chunks:
                print(f"Top chunk: {chunks[0]['content'][:100]}...")
            else:
                print("No chunks found.")
        if chunks:
            print(f"Top chunk: {chunks[0]['content'][:100]}...")
        else:
            print("No chunks found. (Is DB populated?)")
            
        # Test Generation
        if chunks:
            print("\nGenerating Answer...")
            answer = rag.generate_answer(query, chunks)
            print(f"Answer: {answer}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
