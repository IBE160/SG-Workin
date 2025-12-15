
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent of 'backend' to path so we can import 'backend.services...'
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

from backend.services.ingestion import IngestionService

load_dotenv()

def ingest_course_index():
    print("🚀 Starting Master Course Index Ingestion...")
    
    file_path = Path("course_index_dump.md")
    if not file_path.exists():
        print(f"File {file_path} not found. Run crawl_course_index.py first.")
        return

    content = file_path.read_text(encoding="utf-8")
    
    # We treat this as a single "Reference" document
    # URL is the master list URL
    doc = {
        "url": "https://www.himolde.no/english/studies/courses/",
        "title": "Master Course Index (All Courses)",
        "content": content,
        "metadata": {
            "source": "generated_crawler",
            "type": "reference"
        }
    }
    
    ingest_service = IngestionService()
    
    # Use internal method or modify process_and_store to handle single doc
    # process_and_store expects a list
    print(f"Ingesting {len(content)} bytes...")
    result = ingest_service.process_and_store([doc])
    
    print("✅ Ingestion Complete!")
    print(result)

if __name__ == "__main__":
    ingest_course_index()
