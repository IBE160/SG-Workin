import pytest
from unittest.mock import AsyncMock, MagicMock, patch
# Import will fail initially
from backend.services.rag import RagService

@pytest.fixture
def mock_supabase():
    return MagicMock()

@pytest.fixture
def mock_genai():
    with patch("backend.services.rag.genai") as mock:
        yield mock

@pytest.fixture
def rag_service(mock_supabase):
    with patch("backend.services.rag.create_client", return_value=mock_supabase):
        service = RagService()
        return service

import asyncio

def test_search_similar_chunks(rag_service, mock_supabase, mock_genai):
    # Setup
    query = "test query"
    mock_embedding = [0.1, 0.2, 0.3]
    
    # Mock Gemini embedding
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_genai.embed_content.return_value = {"embedding": mock_embedding}

    # Mock Supabase RPC
    mock_rpc = MagicMock()
    mock_supabase.rpc.return_value = mock_rpc
    mock_rpc.execute.return_value.data = [
        {"id": 1, "content": "chunk 1", "similarity": 0.9, "metadata": {}},
        {"id": 2, "content": "chunk 2", "similarity": 0.8, "metadata": {}}
    ]

    # Act
    # Run async method synchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(rag_service.search_similar_chunks(query))
    finally:
        loop.close()

    # Assert
    # Check if Gemini was called
    mock_genai.embed_content.assert_called_once()
    
    # Check if Supabase RPC was called
    mock_supabase.rpc.assert_called_once_with(
        "match_documents",
        {
            "query_embedding": mock_embedding,
            "match_threshold": 0.5,
            "match_count": 5
        }
    )
    
    assert len(results) == 2
    assert results[0]["content"] == "chunk 1"

def test_generate_answer(rag_service, mock_genai):
    # Setup
    query = "What is X?"
    context_chunks = [{"content": "X is Y"}, {"content": "X is also Z"}]
    mock_model = MagicMock()
    mock_genai.GenerativeModel.return_value = mock_model
    mock_response = MagicMock()
    mock_response.text = "X is Y and Z"
    mock_model.generate_content.return_value = mock_response

    # Act
    answer = rag_service.generate_answer(query, context_chunks)

    # Assert
    mock_genai.GenerativeModel.assert_called_with("gemini-2.0-flash-exp") # Or whatever model is used
    mock_model.generate_content.assert_called()
    assert answer == "X is Y and Z"

