import sys
import os
import io

# Add backend to path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'backend')) # For main.py imports


from fastapi.testclient import TestClient
from backend.main import app

def test_endpoint():
    client = TestClient(app)
    
    print("🤖 Testing Chat Endpoint Ambiguity...\n")
    
    # 1. Ambiguous Query
    query = "business"
    print(f"Sending Query: '{query}'")
    response = client.post("/api/chat", json={"message": query})
    
    if response.status_code == 200:
        data = response.json()
        print("Response:", data)
        if data['data']['type'] == 'clarification':
             print("✅ Success: Received clarification request.")
        else:
             print("❌ Failed: Did not receive clarification.")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        
    print("-" * 20)

    # 2. Specific Query (mocking RAG part might fail if no DB connection, but ambiguity check happens first)
    # We expect RAG failure or success, but type should be 'answer' or error, not clarification (unless rector is ambiguous now)
    query = "Who is the rector?"
    print(f"Sending Query: '{query}'")
    response = client.post("/api/chat", json={"message": query})
    print("Response Status:", response.status_code)
    # Note: This might fail in RAG step if DB is not reachable from TestClient env without proper env vars, 
    # but we are testing ambiguity path mainly.

if __name__ == "__main__":
    test_endpoint()
