
import os
import requests
from dotenv import load_dotenv

# Load from backend root .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment.")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print(f"Querying: {url.replace(api_key, 'HIDDEN')}")

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    print("\nAvailable Embedding Models:")
    for model in data.get('models', []):
        if "embedContent" in model.get("supportedGenerationMethods", []) or "embedText" in model.get("supportedGenerationMethods", []):
            print(f"- {model['name']} ({model['version']})")
        
except Exception as e:
    print(f"Error: {e}")
    if 'response' in locals():
        print(response.text)
