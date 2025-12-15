from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock, patch
from backend.main import app

# We will need to patch the usage of RagService in the router
# Since we haven't implemented it yet, we assume the router will import RagService from backend.services.rag

from routers.chat import get_rag_service

def test_chat_rag_integration():
    mock_service_instance = MagicMock()
    # search_similar_chunks is async
    mock_service_instance.search_similar_chunks = AsyncMock(return_value=[{"content": "chunk"}])
    # generate_answer is sync
    mock_service_instance.generate_answer.return_value = "RAG Answer"

    # Use dependency override
    app.dependency_overrides[get_rag_service] = lambda: mock_service_instance

    try:
         client = TestClient(app)
         response = client.post("/api/chat", json={"message": "Query"})
         
         assert response.status_code == 200
         data = response.json()
         assert data["data"]["response"] == "RAG Answer"
    finally:
        app.dependency_overrides.clear()
