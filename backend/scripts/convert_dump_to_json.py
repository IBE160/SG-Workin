
import json
import re
from pathlib import Path

def convert_dump_to_json():
    md_path = Path("course_index_dump.md")
    json_path = Path("backend/data/course_links.json")
    
    if not md_path.exists():
        print("Error: course_index_dump.md not found.")
        return
        
    content = md_path.read_text(encoding="utf-8")
    
    # Regex to extract [Name](URL)
    # Line format: * [CODE Name (Sem Year)](URL)
    # We want to map "CODE" -> URL. 
    # But wait, courses have multiple years.
    # We should probably map "CODE" -> "Latest URL" or specific URL?
    # Or map "CODE Name" -> URL.
    
    # The scraper uses regex: `match = re.match(r"^([A-Z]{3}\d{3})\s+(.*)", clean_line)`
    # It identifies the course by CODE (e.g. LOG206).
    # If there are multiple LOG206, which one to use?
    # Ideally the most recent one? Or the one matching the current year?
    # Let's collect ALL and pick the latest year (2025/2026/2027).
    
    course_versions = {} # CODE -> list of (year, season_num, url)
    course_map = {} # Initialize the map
    
    lines = content.splitlines()
    pattern = re.compile(r"\* \[(.*?)\]\((.*?)\)")
    
    # Season mapping for sorting: Spring=1, Autumn=2
    season_map = {"Spring": 1, "Autumn": 2}
    
    for line in lines:
        match = pattern.search(line)
        if match:
            text = match.group(1) # "LOG206 Digital... (Spring 2026)"
            url = match.group(2)
            
            # Extract Code
            code_match = re.search(r"^([A-Z]{3}[A-Z0-9-]{3,})", text)
            if code_match:
                code = code_match.group(1)
                
                # Extract Semester: (Spring 2026) or (Autumn 2025)
                sem_match = re.search(r"\((Spring|Autumn)\s+(\d{4})\)", text)
                if sem_match:
                    season = sem_match.group(1)
                    year = int(sem_match.group(2))
                    
                    if code not in course_versions:
                        course_versions[code] = []
                    
                    course_versions[code].append({
                        "year": year,
                        "season": season_map.get(season, 0),
                        "url": url,
                        "text": text
                    })

    # Select best version for each course
    # Rule: Maximize (Year, Season)
    count = 0
    name_map = {} # Name -> URL
    
    for code, versions in course_versions.items():
        # Sort desc by year, then season
        versions.sort(key=lambda x: (x["year"], x["season"]), reverse=True)
        
        # Pick the latest one
        best = versions[0]
        course_map[code] = best["url"]
        
        # Update Name Map
        # Extract Name from "LOG206 Digital Business Management (Spring 2026)"
        # Regex: CODE Name (Sem Year)
        # We want just "Name".
        full_text = best["text"]
        # Remove Code
        name_text = full_text.replace(code, "").strip()
        # Remove (Sem Year)
        name_text = re.sub(r"\s+\(.*\)$", "", name_text).strip()
        
        name_map[name_text] = best["url"]
        # Also map lowercase for fuzzy lookup
        name_map[name_text.lower()] = best["url"]
        
        count += 1
        
        if code == "LOG206":
            print(f"DEBUG LOG206: Found {len(versions)} versions. Selected: {best['text']} -> {best['url']}")
    
    print(f"Extracted {count} optimal links.")
    
    # Save Name Map
    name_json_path = Path("backend/data/course_name_map.json")
    with open(name_json_path, "w", encoding="utf-8") as f:
        json.dump(name_map, f, indent=2)
    print(f"Saved Name Map to {name_json_path}")
    
    print(f"Extracted {count} links.")
    print(f"Unique Coedes: {len(course_map)}")
    
    if "LOG206" in course_map:
        print(f"✅ LOG206 mapped to: {course_map['LOG206']}")
    else:
        print("❌ LOG206 NOT found in map.")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(course_map, f, indent=2)
        
    print(f"Saved to {json_path}")

if __name__ == "__main__":
    convert_dump_to_json()
