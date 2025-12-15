
import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load env vars
load_dotenv("backend/.env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in environment.")
    sys.exit(1)

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Creating feedback table...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS feedback (
            id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            term TEXT,
            score INTEGER CHECK (score >= 1 AND score <= 10),
            comment TEXT,
            chat_id uuid
        );
        """
        
        cur.execute(create_table_sql)
        conn.commit()
        
        print("✅ Table 'feedback' created successfully.")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
