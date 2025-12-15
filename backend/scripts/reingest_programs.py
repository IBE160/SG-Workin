
import asyncio
import sys
import os

sys.path.append(os.getcwd())
from backend.services.ingestion import IngestionService
from backend.services.scraper import ScraperService
import logging

# Configure logging to see output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def reingest():
    print("Starting re-ingestion of 'https://www.himolde.no/studier/programmer/'...")
    
    ingestion = IngestionService()
    scraper = ScraperService()
    
    # Scrape fresh content with links
    docs = scraper.scrape_url("https://www.himolde.no/studier/programmer/")
    print(f"Scraped {len(docs)} documents.")
    
    if docs:
        print(f"Processing and storing {len(docs)} documents...")
        ingestion.process_and_store(docs)
            
        print("✅ Re-ingestion complete.")
    else:
        print("❌ Scraper returned no documents.")

if __name__ == "__main__":
    asyncio.run(reingest())
