import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from supabase import create_client, Client

def load_env_manual():
    env_path = Path(__file__).parent.parent / ".env"
    print(f"Reading env from: {env_path}")
    env_vars = {}
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def update_admin_email():
    env = load_env_manual()
    url = env.get("SUPABASE_URL")
    key = env.get("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not key:
        print("Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")
        return

    print("Connecting to Supabase...")
    supabase: Client = create_client(url, key)
    
    print("Listing users...")
    response = supabase.auth.admin.list_users()
    users = response.users if hasattr(response, "users") else response
    
    target_email = "admin@himolde.no"
    new_email = "admin@ibe160.himolde.no"
    
    admin_user = None
    for u in users:
        if u.email == target_email:
            admin_user = u
            break
            
    if not admin_user:
        print(f"User {target_email} not found!")
        for u in users:
            if u.email == new_email:
                print(f"User {new_email} already exists. ID: {u.id}")
                return
        return

    print(f"Found user: {admin_user.email} (ID: {admin_user.id})")
    print(f"Updating to: {new_email}")
    
    try:
        supabase.auth.admin.update_user_by_id(
            admin_user.id,
            {"email": new_email, "email_confirm": True}
        )
        print("Update success!")
    except Exception as e:
        print(f"Update failed: {e}")

if __name__ == "__main__":
    update_admin_email()
