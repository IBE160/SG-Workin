
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def debug_coverage():
    rag = RagService()
    query = "Hei, hvilke årsstudier tilbyr dere?"
    
    # Force limit=50 as per chat.py logic
    limit = 50 
    
    print(f"--- Debugging Coverage for: '{query}' (Limit: {limit}) ---")
    
    chunks = await rag.search_similar_chunks(query, limit=limit, threshold=0.45)
    
    print(f"\nRetrieved {len(chunks)} chunks.")
    
    unique_urls = set()
    programs_found = []
    
    for c in chunks:
        url = c.get('url', '')
        if url not in unique_urls:
            unique_urls.add(url)
            # Simple heuristic to extract program name from URL or content
            title = c.get('title', 'No Title')
            content = c.get('content', '')[:50].replace('\n', ' ')
            programs_found.append(f"{url} | {title} | {content}")
            
    with open("backend/scripts/coverage_report.md", "w", encoding="utf-8") as f:
        f.write(f"# Coverage Report for '{query}'\n\n")
        f.write(f"Chunks Retrieved: {len(chunks)}\n")
        f.write(f"Unique URLs: {len(unique_urls)}\n\n")
        
        f.write("| # | Program/URL | Preview |\n")
        f.write("|---|---|---|\n")
        for i, p in enumerate(sorted(programs_found)):
             # p was formatted as "url | title | content"
             parts = p.split(" | ", 2)
             url = parts[0]
             title = parts[1]
             content = parts[2] if len(parts) > 2 else ""
             f.write(f"| {i+1} | [{title}]({url}) | {content} |\n")
             
    print("Report written to backend/scripts/coverage_report.md")

if __name__ == "__main__":
    asyncio.run(debug_coverage())
