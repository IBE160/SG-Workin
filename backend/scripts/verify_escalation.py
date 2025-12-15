
import requests
import json
import sys

# Change if running on different port
API_URL = "http://127.0.0.1:8000/api/chat"

def verify_escalation():
    # Nonsense query to force fallback
    query = "blurb flurb x99999 what is the capital of mars?"
    
    payload = {
        "message": query,
        "history": []
    }
    
    print(f"Asking nonsense: '{query}'")
    
    try:
        resp = requests.post(API_URL, json=payload)
        data = resp.json()
        
        answer = data["data"]["response"]
        print(f"\n--- Model Response ---\n{answer}\n----------------------")
        
        # Check for contact link
        contact_link = "https://www.himolde.no/kontakt-oss/"
        
        if contact_link in answer:
            print(f"✅ PASS: Response contains contact link: {contact_link}")
        else:
            print(f"❌ FAIL: Response MISSING contact link: {contact_link}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_escalation()
