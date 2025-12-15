
import requests
import json
import uuid

API_URL = "http://127.0.0.1:8000/api/feedback"

def test_feedback():
    payload = {
        "score": 9, 
        "comment": "Great test via API!",
        "chat_id": str(uuid.uuid4())
    }
    
    print(f"Sending payload: {payload}")
    
    try:
        resp = requests.post(API_URL, json=payload)
        if resp.status_code == 200:
            print("✅ API Request Success")
            print(f"Response: {resp.json()}")
        else:
            print(f"❌ API Request Failed: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_feedback()
