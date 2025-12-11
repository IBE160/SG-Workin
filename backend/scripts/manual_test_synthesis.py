import os
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.services.rag import RagService

def test_synthesis():
    rag = RagService()
    
    query = "What are the admission requirements for the PhD program?"
    
    # Mock chunks representing different parts of the answer found on different pages
    mock_chunks = [
        {"content": "For the PhD program in Logistics, applicants must have a Master's degree in a relevant field."},
        {"content": "All PhD applicants must submit a project proposal and three letters of recommendation."},
        {"content": "International PhD students must verify English proficiency via TOEFL or IELTS."}
    ]
    
    print(f"Query: {query}")
    print("Context Chunks:")
    for chunk in mock_chunks:
        print(f"- {chunk['content']}")
        
    print("\nGenerating Answer...\n")
    
    response = rag.generate_answer(query, mock_chunks)
    
    print("-" * 20)
    print(response)
    print("-" * 20)

if __name__ == "__main__":
    test_synthesis()
