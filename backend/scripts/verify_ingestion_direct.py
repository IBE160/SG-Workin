import sys
import os
import logging

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ingestion import IngestionService
from services.scraper import ScraperService

# Setup Logging to see errors
logging.basicConfig(level=logging.INFO)

def verify_direct():
    print("Verifying IngestionService directly...")
    service = IngestionService()
    
    # Create a mock document
    mock_docs = [
        {
            "title": "Test Program",
            "url": "https://www.himolde.no/test-program",
            "description": "A test program description.",
            "content": "This is a test content for the embedding service. It should be chunked and embedded.\n" * 10,
            "source": "himolde.no"
        }
    ]
    
    try:
        print("Running process_and_store with mock data...")
        result = service.process_and_store(mock_docs)
        print("Result:", result)
        
    except Exception as e:
        print(f"Error during direct verification: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_direct()
