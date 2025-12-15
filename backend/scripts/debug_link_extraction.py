
import sys
import os
sys.path.append(os.getcwd())
from backend.services.scraper import ScraperService

def test_real_scraper(url):
    print(f"Testing ScraperService on {url}...")
    scraper = ScraperService()
    
    # We use scrape_url (public wrapper) -> scrape_page_details
    docs = scraper.scrape_url(url)
    
    if not docs:
        print("❌ Scraper returned no docs.")
        return

    main_doc = docs[0]
    content = main_doc.get("content", "")
    
    print("\n--- CONTENT PREVIEW ---")
    print(content[:500])
    
    # Check for Markdown Links
    if "[Årsstudium i" in content and "](" in content:
            print("\n✅ SUCCESS: Found Markdown links in scraper output!")
            # Count them
            count = content.count("](")
            print(f"Found {count} Markdown links.")
    else:
            print("\n❌ FAILED: Still seeing plain text or no Markdown links.")

if __name__ == "__main__":
    test_real_scraper("https://www.himolde.no/studier/programmer/")
