
import logging
import sys
import os
import asyncio

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from backend.services.ingestion import IngestionService
from backend.services.scraper import ScraperService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def surgical_ingest():
    """Ingest specific programs that contain IBE450 to update the URL."""
    scraper = ScraperService()
    ingestor = IngestionService()
    
    # Bachelor in Logistics likely contains IBE450 (which seems to be Logistics related?)
    # or general course pages if we scraped them top-level. 
    # But since we know it's recursive, we target the program.
    # Searching Himolde site, IBE450 is often in "Bachelor i bærekraftig logistikk og sirkulær økonomi" or similar.
    # Let's try to update a few key logistics programs.
    
    target_urls = [
         # Guessing likely candidates based on previous output
         "https://www.himolde.no/studier/programmer/berekraftig-logistikk-og-sirkuler-okonomi/",
         "https://www.himolde.no/studier/programmer/logistikk-scm/",
         "https://www.himolde.no/studier/programmer/petroleumslogistikk-og-%C3%B8konomi/"
    ]
    
    docs_to_ingest = []
    
    for url in target_urls:
        logger.info(f"Surgically scraping: {url}")
        details = scraper.scrape_page_details(url)
        if details:
            docs_to_ingest.append(details)
            
    if docs_to_ingest:
        logger.info(f"Ingesting {len(docs_to_ingest)} updated documents...")
        ingestor.process_and_store(docs_to_ingest)
        logger.info("✅ Surgical ingestion complete.")
    else:
        logger.warning("❌ Failed to scrape target pages.")

if __name__ == "__main__":
    surgical_ingest()
