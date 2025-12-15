
import asyncio
import sys
import os
import logging

# Add backend to path
sys.path.append(os.getcwd())

from backend.services.rag import RagService

logging.basicConfig(level=logging.INFO)

async def debug_courses():
    rag = RagService()
    query = "hvilke fag inngår i årsstudium logistikk?"
    
    # We increased limit to 100 for list queries, but does this query trigger "is_list_query"?
    # "hvilke fag" is in the keywords list. So prompt should use limit=100.
    limit = 100
    
    print(f"--- Debugging Courses for: '{query}' ---")
    
    chunks = await rag.search_similar_chunks(query, limit=limit, threshold=0.45)
    
    print(f"\nRetrieved {len(chunks)} chunks.")
    
    # Check for "Vår" (Spring) vs "Høst" (Autumn) mentions in "logistikk" context
    semesters_found = {"Høst": 0, "Vår": 0}
    
    with open("backend/scripts/course_debug_report.md", "w", encoding="utf-8") as f:
        f.write(f"# Course Debug Report: '{query}'\n\n")
        
        for i, c in enumerate(chunks):
            content = c.get('content', '')
            url = c.get('url', '')
            
            # Simple semester detection
            has_autumn = "høst" in content.lower()
            has_spring = "vår" in content.lower()
            
            if has_autumn: semesters_found["Høst"] += 1
            if has_spring: semesters_found["Vår"] += 1
            
            # If it looks like a course list or study plan
            if "emne" in content.lower() or "studieplan" in content.lower() or "studiemodell" in url:
                f.write(f"## Chunk {i+1} [Score: {c.get('score', 'N/A')}]\n")
                f.write(f"URL: {url}\n")
                f.write(f"Contains: Autumn={has_autumn}, Spring={has_spring}\n")
                f.write("```\n")
                f.write(content.replace('\n', ' ')[:300] + "...")
                f.write("\n```\n\n")

    print(f"Semesters found in chunks: {semesters_found}")
    print("Detailed report written to backend/scripts/course_debug_report.md")

if __name__ == "__main__":
    asyncio.run(debug_courses())
