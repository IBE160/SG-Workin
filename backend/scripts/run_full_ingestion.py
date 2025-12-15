import sys
import os
import logging
import time

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
# Explicitly load .env from backend directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

from backend.services.ingestion import IngestionService
from backend.services.scraper import ScraperService

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_ingestion():
    logger.info("🚀 Starting Full Ingestion Pipeline...")
    start_time = time.time()

    # 1. Scrape
    logger.info("📡 Step 1: Scraping University Website...")
    scraper = ScraperService()
    try:
        programs = scraper.scrape_everything()
        logger.info(f"✅ Scraped {len(programs)} documents.")
    except Exception as e:
        logger.error(f"❌ Scraping failed: {e}")
        return

    if not programs:
        logger.warning("⚠️ No programs found. Exiting.")
        return

    # 2. Ingest
    logger.info("💾 Step 2: Ingesting into Vector Database...")
    ingestor = IngestionService()
    try:
        stats = ingestor.process_and_store(programs)
        logger.info(f"✅ Ingestion Complete. Stats: {stats}")
    except Exception as e:
        import traceback
        logger.error(f"❌ Ingestion failed: {e}")
        traceback.print_exc()
        return

    elapsed = time.time() - start_time
    logger.info(f"🎉 Pipeline finished in {elapsed:.2f} seconds.")

if __name__ == "__main__":
    run_ingestion()
