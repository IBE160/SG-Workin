import asyncio
import os
import sys
from supabase import create_client, Client

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings

async def verify_vector_db():
    print("Verifying Supabase Vector DB Setup...")
    
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_SERVICE_ROLE_KEY
    
    if not url or not key:
        print("Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")
        return

    supabase: Client = create_client(url, key)

    # 1. Verify Connection
    print("1. Connecting to Supabase...")
    try:
        # Simple read to check connection
        supabase.table("document_chunks").select("id").limit(1).execute()
        print("   Connection Successful.")
    except Exception as e:
        print(f"   Connection Failed: {e}")
        return

    # 2. Test Insert with Vector
    print("2. Testing Insert...")
    dummy_embedding = [0.1] * 768 # 768 dimensions
    data = {
        "url": "test_verification",
        "chunk_index": 0,
        "content": "This is a test chunk for verification.",
        "metadata": {"source": "script"},
        "embedding": dummy_embedding
    }
    
    try:
        response = supabase.table("document_chunks").insert(data).execute()
        print(f"   Insert Successful. ID: {response.data[0]['id']}")
        inserted_id = response.data[0]['id']
    except Exception as e:
        print(f"   Insert Failed: {e}")
        return

    # 3. Test Vector Search (RPC or via Client filter if supported, but usually RPC is used for similarity)
    # However, supabase-js/py supports `match_documents` if the function exists. 
    # But standard client insert/select proves the table structure.
    # We will try a simple select for now as RPC 'match_documents' might not exist yet.
    # Verification of *vector* functionality specifically usually requires the RPC function to be created in SQL.
    # Story 2.1 Task 1 did NOT specify creating a match_documents function, only table and index.
    # So we will skip RPC call and just rely on Insert success of vector data as proof of pgvector support (it would fail if vector type missing).
    
    print("3. Vector Storage Verified (Insert succeeded)")

    # 4. Cleanup
    print("4. Cleaning up...")
    try:
        supabase.table("document_chunks").delete().eq("id", inserted_id).execute()
        print("   Cleanup Successful.")
    except Exception as e:
        print(f"   Cleanup Failed: {e}")

    print("\nVerification Complete: SUCCESS")

if __name__ == "__main__":
    asyncio.run(verify_vector_db())
