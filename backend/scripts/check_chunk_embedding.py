
import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv("backend/.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

target_url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/oppbygging/"
print(f"Checking chunk data for: {target_url}")

response = supabase.table("document_chunks").select("id, content, embedding").eq("url", target_url).execute()

chunks = response.data
print(f"✅ Found {len(chunks)} chunks.")

for i, chunk in enumerate(chunks):
    content = chunk["content"]
    embedding = chunk["embedding"]
    print(f"\n--- Chunk {i} ---")
    print(f"Content Start: {content[:100]}")
    if embedding:
        # embedding is a vector (list of floats) or string representation
        if isinstance(embedding, str):
            print(f"✅ Embedding present (Type: str, Len: {len(embedding)})")
        elif isinstance(embedding, list):
            print(f"✅ Embedding present (Type: list, Len: {len(embedding)})")
        else:
            print(f"✅ Embedding present (Type: {type(embedding)})")
    else:
        print("❌ Embedding is MISSING/NULL")
