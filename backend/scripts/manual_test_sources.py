import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.rag import RagService

def test_extract_sources():
    rag = RagService()
    
    # Mock chunks
    mock_chunks = [
        {"content": "Chunk 1", "url": "https://himolde.no/study-a"},
        {"content": "Chunk 2", "url": "https://himolde.no/study-b"},
        {"content": "Chunk 3", "url": "https://himolde.no/study-a"}, # Duplicate URL
        {"content": "Chunk 4", "url": "https://himolde.no/study-c"},
        {"content": "Chunk 5"} # Missing URL
    ]
    
    print("Chunks:")
    for chunk in mock_chunks:
        print(f"- {chunk}")
        
    sources = rag.extract_sources(mock_chunks)
    
    print("\nExtracted Sources:")
    for source in sources:
        print(f"- {source}")
        
    expected = [
        "https://himolde.no/study-a",
        "https://himolde.no/study-b",
        "https://himolde.no/study-c"
    ]
    
    assert sources == expected, f"Expected {expected}, got {sources}"
    print("\n✅ Verification Successful: Sources extracted and deduplicated correctly.")

if __name__ == "__main__":
    test_extract_sources()
