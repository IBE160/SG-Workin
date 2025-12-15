
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")
DATABASE_URL = os.getenv("DATABASE_URL")

def apply_policy():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Applying RLS policy for feedback...")
        
        sql = """
        ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;
        
        -- Drop existing policy if any (to be safe/idempotent)
        DROP POLICY IF EXISTS "Enable insert for anon (public)" ON feedback;
        
        -- Create policy allowing INSERT for anyone (anon role)
        CREATE POLICY "Enable insert for anon (public)"
        ON feedback
        FOR INSERT
        TO anon, authenticated, service_role
        WITH CHECK (true);
        
        -- Also allow reading? Optional, maybe only service_role should read.
        -- Letting anon read might expose other people's feedback. 
        -- So ONLY INSERT for public.
        """
        
        cur.execute(sql)
        conn.commit()
        
        print("✅ RLS Policy 'Enable insert for anon' applied.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Policy application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    apply_policy()
