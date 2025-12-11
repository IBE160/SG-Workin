import sys
import os

# Define base URL
BASE_URL = "http://localhost:8000/api/feedback"

def test_feedback():
    print("Testing Feedback API...")
    
    # 1. Valid Feedback
    payload = {
        "rating": 10,
        "comment": "Great chatbot! Very helpful."
    }
    
    try:
        # We need the server running?
        # Ideally we use TestClient to avoid needing running server
        # Let's import TestClient
        from fastapi.testclient import TestClient
        from fastapi.testclient import TestClient
        import os
        # Add backend to path (parent)
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # Add project root to path (grandparent)
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from backend.main import app
        
        client = TestClient(app)
        
        response = client.post("/api/feedback", json=payload)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Feedback submitted successfully.")
        else:
            print("❌ Failed to submit feedback.")
            print(f"Error: {response.text}")
            sys.exit(1)

    except ImportError as e:
        print(f"ImportError: {e}")
        print("FastAPI TestClient not found. Please install httpx.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_feedback()
