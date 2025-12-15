
import os
import sys
from dotenv import load_dotenv

# Ensure backend modules are found (add 'backend' dir to path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




# Manually load .env to ensure Settings work even if pydantic auto-load fails
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
load_dotenv(env_path, override=True)

from core.config import settings

def main():
    import requests
    
    api_key = settings.GOOGLE_API_KEY
    base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    models_to_test = [
        "models/text-embedding-004",
        "models/gemini-1.5-flash"
    ]
    
    print(f"Testing Standard Models with Key: {api_key[:10]}...")
    
    for model in models_to_test:
        print(f"\n--- Testing {model} ---")
        url = f"{base_url}/{model}:embedContent?key={api_key}"
        payload = {"content": {"parts": [{"text": "hello"}]}, "taskType": "RETRIEVAL_QUERY"}
        
        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                print("SUCCESS!")
                print(resp.json())
            else:
                print(f"Response: {resp.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
