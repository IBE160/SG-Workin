
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Ensure backend modules are found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env')))

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"Connecting to {url} with Service Role Key...")

try:
    supabase = create_client(url, key)
    
    test_url = "https://www.himolde.no/test-delete-verification"
    
    print(f"Attempting to delete chunks for url: {test_url}")
    
    # Try delete
    response = supabase.table("document_chunks").delete().eq("url", test_url).execute()
    
    print("Delete successful!")
    print(f"Data: {response.data}")
    
except Exception as e:
    print(f"FAILED to delete: {e}")
    # Print type of error
    print(f"Error Type: {type(e)}")
