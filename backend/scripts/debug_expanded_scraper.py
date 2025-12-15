
import logging
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logging.basicConfig(level=logging.INFO)

from backend.services.scraper import ScraperService

def test_scraper():
    print("Initializing Expanded Scraper...")
    scraper = ScraperService()
    
    # Override sections to just test one for speed, or let it run briefly
    # Let's test just Student Life and a Program to verify course recursion
    scraper.SECTIONS_TO_CRAWL = [
        "https://www.himolde.no/studentliv/", 
        "https://www.himolde.no/studier/programmer/" 
    ]
    
    # Hack to limit crawl size for debug
    original_crawl_section = scraper._crawl_section
    
    def mocked_crawl_section(section_url):
        print(f"DEBUG: Simulating crawl for {section_url}")
        docs = original_crawl_section(section_url)
        # Limit to 2 docs per section for test
        return docs[:2]
        
    scraper._crawl_section = mocked_crawl_section

    documents = scraper.scrape_everything()
    
    print(f"\nFound {len(documents)} documents.")
    for doc in documents:
        print(f"\n--- DOC: {doc['title']} ---")
        print(f"URL: {doc['url']}")
        content_preview = doc['content'][:200].replace('\n', ' ')
        print(f"Content Start: {content_preview}...")
        
        if "--- COURSE:" in doc['content']:
            print(">>> FOUND COURSES! <<<")
            import re
            courses = re.findall(r"--- COURSE: (.*?) ---", doc['content'])
            print(f"Courses found: {courses}")

if __name__ == "__main__":
    test_scraper()
