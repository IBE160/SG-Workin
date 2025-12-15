
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv("backend/.env")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

# The zombie URL found in output
zombie_url = "https://www.himolde.no/studier/programmer/aarsstudium-i-logistikk/"

print(f"Deleting chunks for: {zombie_url}")
response = supabase.table("document_chunks").delete().eq("url", zombie_url).execute()

print(f"Deleted {len(response.data)} chunks.")
