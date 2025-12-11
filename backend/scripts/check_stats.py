import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings
from supabase import create_client

def check_stats():
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    
    try:
        response = supabase.table("document_chunks").select("id", count="exact").execute()
        print(f"Total Chunks in DB: {response.count}")
        
        # Get a sample
        sample = supabase.table("document_chunks").select("*").limit(1).execute()
        if sample.data:
            print("Sample Chunk:", sample.data[0]['url'])
        else:
            print("No chunks found yet.")
            
    except Exception as e:
        print(f"Error checking stats: {e}")

if __name__ == "__main__":
    check_stats()
