
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")
DATABASE_URL = os.getenv("DATABASE_URL")

def debug_rls():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # 1. Check RLS enabled
        cur.execute("SELECT relrowsecurity FROM pg_class WHERE oid = 'feedback'::regclass;")
        rls_enabled = cur.fetchone()[0]
        print(f"RLS Enabled: {rls_enabled}")
        
        # 2. List Policies
        cur.execute("SELECT polname, polpermissive, polroles, polcmd, polqual, polwithcheck FROM pg_policy WHERE polrelid = 'feedback'::regclass;")
        policies = cur.fetchall()
        print("Policies:")
        for p in policies:
            # polroles is an array of OIDs, might be hard to read directly but shows existence
            print(f" - Name: {p[0]}, Command: {p[3]}")
            
        # 3. Grant Permissions explicitely (just in case)
        print("Granting INSERT to anon/authenticated/service_role...")
        cur.execute("GRANT INSERT ON TABLE feedback TO anon, authenticated, service_role;")
        conn.commit()
        print("✅ Grants applied.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")

if __name__ == "__main__":
    debug_rls()
