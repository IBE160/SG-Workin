import google.generativeai as genai
from supabase import create_client, Client
from backend.core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential

class RagService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        self.embedding_model = "models/text-embedding-004"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def search_similar_chunks(self, query_text: str, limit: int = 5, threshold: float = 0.5):
        """
        Generates an embedding for the query and searches utilizing the 'match_documents' RPC.
        """
        # Generate embedding
        result = genai.embed_content(
            model=self.embedding_model,
            content=query_text,
            task_type="retrieval_query"
        )
        query_embedding = result['embedding']

        # Call Supabase RPC
        response = self.supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": limit
            }
        ).execute()

        return response.data

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_answer(self, query: str, context_chunks: list) -> str:
        """
        Generates an answer based on the provided query and context chunks using Gemini.
        """
        if not context_chunks:
            return "I couldn't find any relevant information to answer your question."

        context_text = "\n\n".join([chunk.get('content', '') for chunk in context_chunks])
        
        prompt = (
            "You are a helpful assistant for University of Molde (HiMolde). "
            "Answer the query based ONLY on the following context. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context_text}\n\n"
            f"Query: {query}"
        )

        try:
            # Using Gemini 2.0 Flash as per Story/Test intent (assuming verified model)
            # If fails, could fallback to gemini-1.5-flash
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Log error?
            return "I'm having trouble connecting to my knowledge base right now."

