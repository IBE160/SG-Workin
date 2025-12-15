
import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path
import time

def crawl_filtered_courses():
    base_url = "https://www.himolde.no/studier/emner/"
    
    # We want active courses: Autumn 2025 (h25) and Spring 2026 (v26)
    # And both languages.
    scenarios = [
        {"sem": "v26", "lang": "Norwegian", "label": "Spring 2026 (NO)"},
        {"sem": "h25", "lang": "Norwegian", "label": "Autumn 2025 (NO)"},
        {"sem": "v26", "lang": "English", "label": "Spring 2026 (EN)"},
        {"sem": "h25", "lang": "English", "label": "Autumn 2025 (EN)"}
    ]
    
    course_db = {
        "codes": {}, # CODE -> URL
        "names": {}  # NAME (lowercased) -> URL
    }
    
    headers = {
        "User-Agent": "ibe160-chatbot-crawler/0.1"
    }

    for sc in scenarios:
        print(f"Crawling {sc['label']}...")
        # Construct URL
        # Note: Parameters need to be precise.
        # Based on user input: ?filter.semesters=v26&filter.resource%3Afs@language=Norwegian
        url = f"{base_url}?filter.semesters={sc['sem']}&filter.resource%3Afs@language={sc['lang']}"
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, "html.parser")
            
            # Helper to find links. Adjust selector based on actual page structure.
            # Usually strict lists have a specific class or check all links in 'main'.
            # From debug_structure_html, we saw standard <a> tags.
            
            # The structure might be a table or a list.
            # Let's assume standard link extraction and filtering for "/studier/emner/"
            
            links = soup.find_all("a", href=True)
            count = 0
            for link in links:
                href = link["href"]
                # Check strict path
                if "/studier/emner/" in href or "/english/studies/courses/" in href:
                    text = link.get_text(strip=True)
                    # "IBE110 Informasjonsteknologi"
                    
                    # Extract Code
                    code_match = re.search(r"([A-Z]{3}\d{3})", text)
                    if code_match:
                        code = code_match.group(1)
                        full_url = requests.compat.urljoin(base_url, href)
                        
                        # 1. Map Code -> URL (Latest overwrites? h25 vs v26?)
                        # We process v26 first in scenarios list? No.
                        # Actually v26 is "later" than h25.
                        # Let's prefer v26.
                        # If we already have a v26 link, don't overwrite with h25?
                        # Simplification: Just overwrite. User wants "Active".
                        course_db["codes"][code] = full_url
                        
                        # 2. Map Name -> URL
                        # Extract Name Part
                        # "LOG206 Digital Business Management" -> "Digital Business Management"
                        # Also strip "(Spring 2026)" or "(Vår 2026)"
                        name_text = text.replace(code, "").strip()
                        # Regex to remove parens with semester info
                        name_text = re.sub(r"\s*\(.*\)", "", name_text).strip()
                        
                        if name_text:
                             course_db["names"][name_text.lower()] = full_url
                        
                        count += 1
            
            print(f"  Found {count} courses.")
            time.sleep(1) # Be polite
            
        except Exception as e:
            print(f"  Failed: {e}")

    # Save DB
    out_path = Path("backend/data/course_database.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(course_db, f, indent=2)
        
    print(f"Saved {len(course_db['codes'])} codes and {len(course_db['names'])} names to {out_path}")

if __name__ == "__main__":
    crawl_filtered_courses()
