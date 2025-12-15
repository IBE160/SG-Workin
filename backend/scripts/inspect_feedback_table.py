
import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'feedback';")
    columns = cur.fetchall()
    print("Feedback Table Columns:")
    for col in columns:
        print(f" - {col[0]} ({col[1]})")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
