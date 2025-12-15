
from dotenv import load_dotenv
import os
import sys

# Add project root to sys.path (3 levels up: scripts -> backend -> root)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path, override=True)

from backend.core.config import settings
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

print("Verifying DB Content...")
try:
    response = supabase.table("document_chunks").select("id, url, metadata").limit(5).execute()
    if response.data:
        print(f"Found {len(response.data)} chunks.")
        for chunk in response.data:
            print(f"ID: {chunk['id']}")
            print(f"URL: {chunk['url']}")
            print(f"Metadata: {chunk['metadata']}")
            print("-" * 20)
    else:
        print("No chunks found in DB.")
except Exception as e:
    print(f"Error: {e}")
