
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(str(Path.cwd()))

load_dotenv("backend/.env")

from backend.services.scraper import ScraperService
from backend.services.ingestion import IngestionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_page(url: str):
    print(f"🚀 Ingesting Single Page: {url}")
    
    scraper = ScraperService()
    docs = scraper.scrape_url(url)
    
    if not docs:
        print("❌ No content scraped.")
        return

    print(f"📄 Scraped {len(docs)} documents/chunks from page.")
    
    ingestor = IngestionService()
    result = ingestor.process_and_store(docs)
    
    print(f"✅ Ingestion Result: {result}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_single_page.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    ingest_page(url)
