import sys
import os
import asyncio
import logging

# Setup path
sys.path.append(os.getcwd())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debug_system")

async def main():
    print("1. Checking imports...")
    try:
        import httpx
        print("   [OK] httpx built-in/installed")
    except ImportError:
        print("   [FAIL] httpx not found")
        
    try:
        from supabase import create_client
        print("   [OK] supabase-py installed")
    except ImportError:
        print("   [FAIL] supabase-py not found")

    print("\n2. Checking Supabase Connection...")
    from backend.core.config import settings
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        response = supabase.table("document_chunks").select("count", count="exact").limit(1).execute()
        print(f"   [OK] Connection successful. Count: {response.count}")
    except Exception as e:
        print(f"   [FAIL] Supabase connection error: {e}")

    print("\n3. Checking RagService Instantiation...")
    try:
        from backend.services.rag import RagService
        service = RagService()
        print("   [OK] RagService initialized")
    except Exception as e:
        print(f"   [FAIL] RagService init error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
