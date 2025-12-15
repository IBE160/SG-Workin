
import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv("backend/.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

good_url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/" # Rank 1 (Main Page)
bad_url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/oppbygging/" # Missing

print(f"Fetching Good Chunk: {good_url}")
good_resp = supabase.table("document_chunks").select("id, embedding, content").eq("url", good_url).limit(1).execute()

print(f"Fetching Bad Chunk: {bad_url}")
bad_resp = supabase.table("document_chunks").select("id, embedding, content").eq("url", bad_url).limit(1).execute()

if good_resp.data:
    g = good_resp.data[0]
    print(f"✅ Good Chunk content len: {len(g['content'])}")
    print(f"✅ Good Chunk embedding type: {type(g['embedding'])}")
    if isinstance(g['embedding'], str):
         print(f"✅ Good Chunk embedding len: {len(g['embedding'])}")
         print(f"Sample: {g['embedding'][:50]}...")
    elif isinstance(g['embedding'], list):
         print(f"✅ Good Chunk embedding vector len: {len(g['embedding'])}")
else:
    print("❌ Good Chunk not found (unexpected)")

if bad_resp.data:
    b = bad_resp.data[0]
    print(f"✅ Bad Chunk content len: {len(b['content'])}")
    print(f"✅ Bad Chunk embedding type: {type(b['embedding'])}")
    if isinstance(b['embedding'], str):
         print(f"✅ Bad Chunk embedding len: {len(b['embedding'])}")
         print(f"Sample: {b['embedding'][:50]}...")
    elif isinstance(b['embedding'], list):
         print(f"✅ Bad Chunk embedding vector len: {len(b['embedding'])}")
else:
    print("❌ Bad Chunk not found")
