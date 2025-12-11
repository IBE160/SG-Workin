import logging
import google.generativeai as genai
from supabase import create_client, Client
from backend.core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.schemas.chat import ChatMessage

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self):
        # Configuration should ideally be done in main/lifespan, but staying scopes:
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
        
        prompt = settings.RAG_SYSTEM_PROMPT.format(
            context_text=context_text,
            query=query
        )

        try:
            # Using Gemini 2.0 Flash as per Story/Test intent (assuming verified model)
            # If fails, could fallback to gemini-1.5-flash
            model = genai.GenerativeModel(settings.GEMINI_MODEL) # Use configured model
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {e}"

    def detect_ambiguity(self, query: str) -> dict:
        """Check if query is ambiguous and return clarification if needed."""
        prompt = settings.AMBIGUITY_SYSTEM_PROMPT.format(query=query)
        
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL) # Use configured model
            response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            import json
            return json.loads(response.text)
        except Exception as e:
            logger.warning(f"Ambiguity check failed: {e}")
            return {"is_ambiguous": False}

    def contextualize_query(self, query: str, history: list[ChatMessage]) -> str:
        """Rewrite query to be self-contained based on history."""
        if not history:
            return query
            
        # Format history for prompt
        history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
        
        prompt = settings.CONTEXTUALIZE_SYSTEM_PROMPT.format(
            history=history_text,
            query=query
        )
        
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            # Generate the rewritten query
            response = model.generate_content(prompt)
            rewritten = response.text.strip()
            logger.info(f"Contextualized Query: '{query}' -> '{rewritten}'")
            return rewritten
        except Exception as e:
            logger.error(f"Contextualization failed: {e}")
            return query

    def extract_sources(self, chunks: list[dict]) -> list[str]:
        """Extract unique URLs from chunks."""
        if not chunks:
            return []
        
        # Extract 'url' from chunks, remove duplicates while preserving order (roughly)
        urls = []
        seen = set()
        
        for chunk in chunks:
            url = chunk.get("url")
            if url and url not in seen:
                seen.add(url)
                urls.append(url)
        
        return urls
