
import requests
from bs4 import BeautifulSoup
import time
import sys

def crawl_course_index():
    base_url = "https://www.himolde.no/english/studies/courses/"
    current_url = base_url
    all_courses = []
    
    seen_urls = set()
    page_num = 1
    
    while current_url:
        print(f"Scraping Page {page_num}: {current_url}")
        try:
            resp = requests.get(current_url, timeout=10)
            if resp.status_code != 200:
                print(f"Failed to fetch {current_url}")
                break
                
            soup = BeautifulSoup(resp.content, "html.parser")
            
            # Extract course links
            # Pattern: /english/studies/courses/...
            links = soup.find_all("a", href=True)
            for a in links:
                href = a['href']
                if "/studies/courses/" in href and "page=" not in href:
                    full_url = "https://www.himolde.no" + href if href.startswith("/") else href
                    text = a.get_text(strip=True)
                    if full_url not in seen_urls:
                        # simple filter to avoid sidebar garbage
                        if len(text) > 5 and any(char.isdigit() for char in text): 
                            all_courses.append((text, full_url))
                            seen_urls.add(full_url)
                            # Check specifically for LOG206
                            if "LOG206" in text or "Digital Business Management" in text:
                                print(f"✅ FOUND TARGET: {text} -> {full_url}")

            # Find Next Page
            # Look for link with text "Next page" or similar, or checking params
            next_link = None
            # The output showed: LINK: Next page -> ...
            for a in links:
                if "Next page" in a.get_text():
                    next_link = a['href']
                    break
            
            if next_link:
                current_url = "https://www.himolde.no" + next_link if next_link.startswith("/") else next_link
                page_num += 1
                time.sleep(1) # Be nice
            else:
                print("No next page found. Finished.")
                current_url = None
                
        except Exception as e:
            print(f"Error: {e}")
            break
            
    print(f"\nTotal Courses Found: {len(all_courses)}")
    
    # Save to file for inspection
    with open("course_index_dump.md", "w", encoding="utf-8") as f:
        f.write("# Master Course Index\n\n")
        f.write(f"Updated: {time.ctime()}\n\n")
        for name, url in sorted(all_courses):
            f.write(f"* [{name}]({url})\n")
    
    print("Saved to course_index_dump.md")

if __name__ == "__main__":
    crawl_course_index()
