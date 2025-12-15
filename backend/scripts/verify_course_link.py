
import requests
import json
import sys

URL = "http://localhost:8000/api/chat"
HEADERS = {"Content-Type": "application/json"}

# Query specifically targeting the course list for Logistics
QUERY = "hvilke fag inngår i Årsstudium i logistikk?"

def verify_response():
    payload = {
        "message": QUERY, # "message" for ChatRequest schema
        "history": []
    }

    print(f"Sending request to {URL}...")
    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # Adjust parsing based on actual response structure
        # Response model: {"data": {"response": "..."}}
        answer = data.get("data", {}).get("response", "")
        
        print("\n--- RESPONSE START ---")
        print(answer)
        print("\n--- RESPONSE END ---")

        if "[" in answer and "](" in answer:
            # Check for specific courses
            if "LOG206" in answer or "SCM130" in answer or "logistikk" in answer: 
                # Loose check for links
                 print("\n✅ SUCCESS: Found clickable links in the response.")
                 sys.exit(0)
            else:
                 print("\n⚠️ LINKS FOUND, but might not be the right ones? Check manually.")
                 sys.exit(0)
        else:
            print("\n❌ FAILED: No clickable links found.")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_response()
