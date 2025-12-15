
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")
DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("Altering feedback table...")
        
        # Add chat_id if not exists
        try:
            cur.execute("ALTER TABLE feedback ADD COLUMN chat_id uuid;")
            print("✅ Added column 'chat_id'.")
        except psycopg2.errors.DuplicateColumn:
            print("ℹ️ Column 'chat_id' already exists.")
            conn.rollback() # Reset transaction
            # Start new transaction
            cur = conn.cursor() 

        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate()
