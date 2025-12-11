import asyncio
import os
import sys

# Add project root to sys.path to allow 'backend' imports
current_dir = os.path.dirname(os.path.abspath(__file__)) # backend/scripts
backend_dir = os.path.dirname(current_dir) # backend
project_root = os.path.dirname(backend_dir) # SG-Workin
sys.path.append(project_root)

from backend.services.rag import RagService

async def main():
    print("🚀 Starting RAG Verification Script")
    print("-----------------------------------")
    
    print("Initializing RagService...")
    try:
         rag = RagService()
    except Exception as e:
         print(f"❌ Failed to initialize RagService: {e}")
         sys.exit(1)
    
    query = "What engineering programs does HiMolde offer?"
    print(f"Testing search with query: '{query}'")
    
    try:
        chunks = await rag.search_similar_chunks(query, limit=3)
        print("✅ Search call executed successfully!")
        print(f"Found {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
             print(f"  [{i+1}] Content preview: {chunk.get('content', '')[:50]}...")
             
    except Exception as e:
        print(f"❌ Search failed: {e}")
        error_msg = str(e).lower()
        if "match_documents" in error_msg or "function not found" in error_msg:
            print("\n⚠️  CRITICAL: The 'match_documents' RPC function is missing in Supabase.")
            print("Please run the SQL migration manually in Supabase Dashboard SQL Editor.")
            print("SQL File: supabase/migrations/20251211193000_match_documents.sql")
        sys.exit(1)

    # Test Answer Generation
    print("\nTesting answer generation...")
    # Mock chunks if search returned nothing (e.g. empty DB) to verify generation logic
    if not chunks:
        print("⚠️ No chunks found (DB might be empty). Using dummy chunk for generation test.")
        chunks = [{"content": "HiMolde offers several engineering programs including Logistics and IT."}]
    
    try:
        answer = rag.generate_answer(query, chunks)
        print(f"✅ Generated Answer: {answer}")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        sys.exit(1)

    print("\n🎉 Verification Complete!")

if __name__ == "__main__":
    asyncio.run(main())
