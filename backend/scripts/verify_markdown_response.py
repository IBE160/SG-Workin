
import requests
import sys

def verify_markdown():
    url = "http://127.0.0.1:8000/api/chat"
    payload = {"message": "Årsstudium i IT, hvilke fag inneholder dette studiet?", "history": []}
    
    print("Sending request...")
    try:
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            response_text = data.get("response", "")
            print("\n--- RESPONSE START ---")
            print(response_text)
            print("--- RESPONSE END ---\n")
            
            if "[" in response_text and "](" in response_text and ")" in response_text:
                print("✅ PASSED: Markdown links detected.")
            else:
                print("❌ FAILED: No Markdown links found.")
        else:
            print(f"Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_markdown()
