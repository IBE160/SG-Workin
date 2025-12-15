import google.generativeai as genai
import os
import sys

# Add project root to path (SG-Workin)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.core.config import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

def list_models():
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")

if __name__ == "__main__":
    list_models()
