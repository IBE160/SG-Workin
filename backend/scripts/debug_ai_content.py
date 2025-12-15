
import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from backend.services.rag import RagService

async def test_ai_retrieval():
    rag = RagService()
    query = "Årsstudium i IT, hvilke fag inneholder dette studiet?"
    print(f"\n--- Searching for: '{query}' ---")
    chunks = await rag.search_similar_chunks(query, limit=30)
    
    found_any_injection = False

    for i, c in enumerate(chunks):
        url = c.get('url', '')
        print(f"\n[{i+1}] {url}")
        
        if "it/oppbygging" in url:
             content = c.get('content', '')
             print(f"--- CONTENT SNIPPET ({len(content)} chars) ---")
             print(content[:300]) 
             
             if "http" in content and "studier/emner" in content:
                  print("✅ Contains Injected URLs")
                  found_any_injection = True
             else:
                  print("❌ No URL injection in this chunk")
             
             idx = content.find("IBE102")
             if idx != -1:
                print(f"Snippet around IBE102: ...{content[idx:idx+200]}...")
             else:
                print("Course IBE102 not found in text.")

    if not found_any_injection:
        print("\n❌ CRITICAL: No retrieved chunks contained injected URLs.")

if __name__ == "__main__":
    asyncio.run(test_ai_retrieval())
