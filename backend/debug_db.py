
import asyncio
from supabase import create_client
from backend.core.config import settings

async def main():
    print("Checking database connection...")
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        
        # Check count
        response = supabase.table("document_chunks").select("count", count="exact").execute()
        print(f"Total chunks in DB: {response.count}")
        
        # Check first 5 items
        data = supabase.table("document_chunks").select("*").limit(5).execute()
        print("First 5 items:")
        for item in data.data:
            print(f"- URL: {item.get('url')}, Title: {item.get('title')}, Metadata: {item.get('metadata')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
