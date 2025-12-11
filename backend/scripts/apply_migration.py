import os
import sys
from sqlalchemy import create_engine, text

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings

def apply_migration():
    print(f"Connecting to database...")
    # Ensure DATABASE_URL is available
    if not settings.DATABASE_URL:
        print("Error: DATABASE_URL not set in settings.")
        sys.exit(1)

    engine = create_engine(settings.DATABASE_URL)
    
    migration_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "supabase", "migrations", "20241211205700_create_feedback_table.sql"
    )
    
    if not os.path.exists(migration_file):
        print(f"Error: Migration file not found at {migration_file}")
        sys.exit(1)
        
    print(f"Reading migration file: {migration_file}")
    with open(migration_file, "r") as f:
        sql = f.read()
        
    print("Executing SQL...")
    with engine.connect() as connection:
        # Split by statements if needed, but simple create table + policy usually works in one block or split by ;
        # However, create_engine usually executes single statement. 
        # For safety, let's split roughly by command or try executing block.
        # Actually sqlalchemy execution of multiple statements might depend on driver.
        # Let's try executing the whole block.
        try:
            connection.execute(text(sql))
            connection.commit()
            print("Migration applied successfully.")
        except Exception as e:
            print(f"Error applying migration: {e}")
            sys.exit(1)

if __name__ == "__main__":
    apply_migration()
