
import asyncio
import sys
import os
import logging
from supabase import create_client

# Add backend to path
sys.path.append(os.getcwd())

from backend.core.config import settings

logging.basicConfig(level=logging.INFO)

def fetch_chunks():
    print("--- Connecting to Supabase directly ---")
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    
    target_url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/oppbygging/"
    
    print(f"Querying chunks for URL: {target_url}")
    
    response = supabase.table("document_chunks") \
        .select("id, chunk_index, content") \
        .eq("url", target_url) \
        .execute()
        
    chunks = response.data
    print(f"Found {len(chunks)} chunks.")
    
    for c in sorted(chunks, key=lambda x: x.get('chunk_index', 0)):
        print(f"\n[Chunk Index: {c.get('chunk_index')}] ID: {c.get('id')}")
        content = c.get('content', '')
        print(f"Length: {len(content)}")
        print(f"Preview Start: {content[:100].replace(chr(10), ' ')}...")
        print(f"Preview End: ...{content[-100:].replace(chr(10), ' ')}")

if __name__ == "__main__":
    fetch_chunks()
