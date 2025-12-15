
import requests
import json
import sys
import re

URL = "http://localhost:8000/api/chat"
HEADERS = {"Content-Type": "application/json"}

def verify_links(query, min_links=1):
    payload = {"message": query, "history": []}
    print(f"\n--- Testing: '{query}' ---")
    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        answer = response.json().get("data", {}).get("response", "")
        print(f"Response Preview: {answer[:300]}...")

        # Regex to find Markdown links: [Text](URL)
        links = re.findall(r'\[([^\]]+)\]\((http[^\)]+)\)', answer)
        
        print(f"Found {len(links)} links.")
        for text, url in links:
            print(f"- {text}: {url}")

        if len(links) >= min_links:
            print(f"✅ PASSED: Found {len(links)} links (min required: {min_links}).")
            return True
        else:
            print(f"❌ FAILED: Found {len(links)} links, expected at least {min_links}.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test 1: Simple Hello to verify model connectivity
    studies_pass = verify_links("hello", min_links=0)
    
    # Test 2: Ignored
    # Asking specific question to trigger retrieval
    life_pass = verify_links("tell me about the student parliament (Studenttinget)", min_links=1)

    if studies_pass and life_pass:
        print("\n🎉 ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("\n💥 SOME CHECKS FAILED")
        sys.exit(1)
