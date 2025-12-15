
import requests
import os
import sys
# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path, override=True)
from backend.core.config import settings

api_key = settings.GOOGLE_API_KEY
base_url = "https://generativelanguage.googleapis.com/v1beta"

models = [
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.0-flash-lite-preview-02-05",
]

print(f"Testing Generation Models with Key: {api_key[:10]}...")

for model in models:
    print(f"\n--- Testing {model} ---")
    url = f"{base_url}/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": "Hello, are you working?"}]}]
    }
    
    try:
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"WORKING MODEL FOUND: {model}")
            break # Stop after first success
        else:
            print(f"Response: {resp.text[:100]}...")
    except Exception as e:
        print(f"Error: {e}")
