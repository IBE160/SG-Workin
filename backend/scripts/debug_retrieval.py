
import asyncio
import os
import sys

# Ensure backend can be imported
sys.path.append(os.getcwd())

from backend.services.rag import RagService
from dotenv import load_dotenv

load_dotenv("backend/.env")

async def debug_retrieval():
    print("Initializing RAG Service...")
    
    rag_service = RagService()
    
    query = "hvilke fag inngår i Årsstudium i logistikk?"
    print(f"\nQuery: {query}")
    
    print("Searching chunks via RagService...")
    chunks = await rag_service.search_similar_chunks(query, limit=50)
    
    print(f"\nFound {len(chunks)} chunks. Writing report to backend/scripts/retrieval_report.md...")
    
    with open("backend/scripts/retrieval_report.md", "w", encoding="utf-8") as f:
        f.write(f"# Retrieval Report\n\nQuery: `{query}`\n\nFound: {len(chunks)} chunks\n\n")
        for i, chunk in enumerate(chunks):
            score = chunk.get("similarity", 0)
            content = chunk.get("content", "")
            url = chunk.get("url", "")
            title = chunk.get("title", "")
            
            f.write(f"## Rank {i+1} (Score: {score:.4f})\n")
            f.write(f"- **Title**: {title}\n")
            f.write(f"- **URL**: {url}\n")
            f.write(f"- **Content Preview**: {content[:200].replace(chr(10), ' ')}...\n") # Replace newline
            if "| [" in content:
                f.write("- **Status**: ✨ CONTAINS MARKDOWN TABLE LINKS\n")
            if "Hva lærer du" in content or "Learning Outcomes" in title:
                f.write("- **Status**: ⚠️ LEARNING OUTCOMES CHUNK\n")
            f.write("\n")

if __name__ == "__main__":
    asyncio.run(debug_retrieval())
