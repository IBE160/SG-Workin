
import requests
import json
import sys

URL = "http://localhost:8000/api/chat"
HEADERS = {"Content-Type": "application/json"}

def test_naming(query, expected_name, lang_label):
    payload = {"message": query, "history": []}
    print(f"\n--- Testing ({lang_label}): '{query}' ---")
    try:
        response = requests.post(URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        answer = response.json().get("data", {}).get("response", "")
        print(f"Response: {answer}")

        if expected_name.lower() in answer.lower():
            print(f"✅ PASSED: Found '{expected_name}'")
            return True
        else:
            print(f"❌ FAILED: Expected '{expected_name}' not found.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test Norwegian
    no_pass = test_naming("hei", "Høgskolen i Molde", "Norwegian")
    
    # Test English
    en_pass = test_naming("hi", "Molde University College", "English")

    if no_pass and en_pass:
        print("\n🎉 ALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("\n💥 SOME CHECKS FAILED")
        sys.exit(1)
