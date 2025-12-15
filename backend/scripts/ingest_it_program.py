
import logging
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from backend.services.ingestion import IngestionService
from backend.services.scraper import ScraperService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_it_program():
    logger.info("🚀 Starting Surgical Ingestion used for testing...")
    
    scraper = ScraperService()
    ingestor = IngestionService()
    
    # We target the IT program & the One Year IT program
    target_urls = [
         "https://www.himolde.no/studier/programmer/it/", 
         "https://www.himolde.no/studier/programmer/it-og-digitalisering/"
    ]
    
    docs_to_ingest = []
    
    for url in target_urls:
        logger.info(f"Scraping: {url}")
        # The new scraper logic creates multiple docs (Main + Structure + Courses)
        docs = scraper.scrape_page_details(url)
        if docs:
            docs_to_ingest.extend(docs)
            
    if docs_to_ingest:
        logger.info(f"Found {len(docs_to_ingest)} documents. Ingesting...")
        ingestor.process_and_store(docs_to_ingest)
        logger.info("✅ Ingestion complete.")
    else:
        logger.warning("❌ No docs found.")

if __name__ == "__main__":
    ingest_it_program()
