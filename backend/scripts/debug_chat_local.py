
import requests
import json

url = "http://127.0.0.1:8000/api/chat"

messages = [
    "what bachelor programs are available"
]

for msg in messages:
    # Specific query: "Årsstudium i IT, hvilke fag inneholder dette studiet?"
    # Expectation: 
    # 1. Source should be .../it/oppbygging/ (or similar sub-page)
    # 2. Answer should list courses with URLs: "Programmering (https://...)"
    payload = {"message": "Årsstudium i IT, hvilke fag inneholder dette studiet?", "history": []}
    try:
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Type: {data.get('data', {}).get('type')}")
        print(f"Response: {data.get('data', {}).get('response')}")
        print(f"Sources: {data.get('data', {}).get('sources')}")
    except Exception as e:
        print(f"Request failed: {e}")
