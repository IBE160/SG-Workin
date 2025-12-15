
import logging
import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from backend.services.ingestion import IngestionService
from backend.services.scraper import ScraperService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ingest_landing_pages():
    logger.info("🚀 Starting Landing Page Ingestion...")
    
    scraper = ScraperService()
    ingestor = IngestionService()
    
    landing_pages = []
    
    # Scrape just the landing pages directly
    for url in scraper.SECTIONS_TO_CRAWL:
        logger.info(f"Scraping landing page: {url}")
        details = scraper.scrape_page_details(url)
        if details:
            # Force a good title if missing
            if "programmer" in url:
                details["title"] = "Oversikt over alle studieprogrammer"
                details["content"] += "\n\nThis page lists all available bachelor and master programs."
            landing_pages.append(details)
            
    if landing_pages:
        logger.info(f"Found {len(landing_pages)} landing pages. Ingesting...")
        ingestor.process_and_store(landing_pages)
        logger.info("✅ Landing pages ingested.")
    else:
        logger.warning("❌ No landing pages found.")

if __name__ == "__main__":
    ingest_landing_pages()
