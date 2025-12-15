import logging
from supabase import create_client, Client
from backend.core.config import settings
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.schemas.chat import ChatMessage
import requests

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        self.embedding_model = "models/text-embedding-004"
        self.generation_model = settings.GEMINI_MODEL
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=0.5, max=5))
    async def search_similar_chunks(self, query_text: str, limit: int = 50, threshold: float = 0.45):
        """
        Generates an embedding for the query and searches utilizing the 'match_documents' RPC.
        Uses REST API to avoid heavy grpcio dependency.
        """
        import requests
        
        try:
            # 1. Generate Embedding via REST
            url = f"{self.base_url}/{self.embedding_model}:embedContent?key={self.api_key}"
            payload = {
                "content": {"parts": [{"text": query_text}]},
                "taskType": "RETRIEVAL_QUERY"
            }
            
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            resp.raise_for_status()
            embedding_data = resp.json()
            
            # Extract embedding vector (values)
            if "embedding" in embedding_data:
                query_embedding = embedding_data["embedding"].get("values")
            else:
                query_embedding = None
        
        except Exception as e:
            error_msg = str(e)
            if hasattr(self, 'api_key') and self.api_key:
                error_msg = error_msg.replace(self.api_key, "HIDDEN_KEY")
            logger.error(f"Failed to generate embedding via REST API: {error_msg}")
            return []

        # 2. Call Supabase RPC
        response = self.supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_threshold": threshold,
                "match_count": limit
            }
        ).execute()
        
        chunks = response.data
        if not chunks:
            return []

        # WORKAROUND: RPC is missing columns. Fetch url and chunk_index via secondary query.
        try:
            chunk_ids = [c['id'] for c in chunks]
            if chunk_ids:
                # 1. Fetch metadata for retrieved chunks
                meta_resp = self.supabase.table("document_chunks") \
                    .select("id, url, chunk_index") \
                    .in_("id", chunk_ids) \
                    .execute()
                
                meta_map = {row['id']: row for row in meta_resp.data}
                
                # Enrich chunks and identify neighbors
                enriched_chunks = []
                neighbor_ids_to_fetch = []
                
                # Group by URL to find localized gaps (optional, but simple neighbor fetch is easier)
                # We'll simple fetch index+1 for every chunk if it's not already in the list.
                
                active_indices = set() # (url, index)
                for row in meta_resp.data:
                    if row.get('url') and row.get('chunk_index') is not None:
                        active_indices.add((row['url'], row['chunk_index']))

                for chunk in chunks:
                    meta = meta_map.get(chunk['id'])
                    if meta:
                        chunk['url'] = meta.get('url')
                        chunk['chunk_index'] = meta.get('chunk_index')
                        
                        # Identify neighbor (Next Chunk)
                        if chunk.get('chunk_index') is not None:
                            next_index = chunk['chunk_index'] + 1
                            url = chunk['url']
                            if (url, next_index) not in active_indices:
                                # Candidate for fetching. 
                                # We need to find the ID of this neighbor. 
                                # We can't fetch by ID because we don't know it. We must query by (url, index).
                                # To avoid N queries, we collect these requirements.
                                neighbor_ids_to_fetch.append({"url": url, "index": next_index})
                    
                    enriched_chunks.append(chunk)

                # 2. Bulk fetch neighbors (if any)
                if neighbor_ids_to_fetch:
                     # Supabase OR syntax is tricky for multiple (url, index) pairs.
                     # Simplified: Just query candidates that match the URLs we have, with index IN [list of indices].
                     # Better: Query all chunks for these URLs where index is in the target set.
                     # Optimization: limit to top 20 chunks to avoid explosion? 
                     # Let's apply this logic only for the Top 20 chunks to keep it fast.
                     
                     targets_to_fetch = neighbor_ids_to_fetch[:20] # fetch neighbors for top 20 only
                     
                     if targets_to_fetch:
                         or_cond = ",".join([f"and(url.eq.{t['url']},chunk_index.eq.{t['index']})" for t in targets_to_fetch])
                         # Supabase-py .or_() method
                         
                         neighbor_resp = self.supabase.table("document_chunks") \
                            .select("id, content, url, chunk_index") \
                            .or_(or_cond) \
                            .execute()
                            
                         for row in neighbor_resp.data:
                             # Add neighbor as a chunk with slightly lower score (or inherit)
                             row['score'] = 0.0 # It's context, not a match
                             row['is_neighbor'] = True
                             enriched_chunks.append(row)
                             logger.info(f"Fetched neighbor chunk: {row['id']} for {row['url']}")

                chunks = enriched_chunks

        except Exception as e:
            logger.error(f"Failed to fetch metadata or neighbors: {e}")

        return chunks

    # 250 RPM = 0.24s interval. Retrying after 1s is safe.
    @retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, min=1, max=10))
    def generate_answer(self, query: str, context_chunks: list) -> str:
        """
        Generates an answer based on the provided query and context chunks using Gemini REST API.
        """
        # FORCE FALLBACK for simple greetings to avoid context pollution (e.g. "Hi" matching "HiM")
        # This ensures the strict Greeting/Persona logic in the fallback prompt is used.
        greetings = {"hi", "hei", "hallo", "hello", "hey", "hvem er du", "who are you"}
        if query.strip().lower().replace("?", "").replace("!", "") in greetings:
            logger.info(f"Greeting detected: '{query}'. Forcing fallback prompt.")
            context_chunks = []

        if not context_chunks:
            # Fallback to general conversation prompt if no context found
            prompt_text = f"""You are the official assistant for Molde University College (Høgskolen i Molde).

            CRITICAL INSTRUCTION: DETECT THE LANGUAGE OF THE USER'S QUERY AND RESPOND IN THAT LANGUAGE.

            ---
            CASE 1: User speaks NORWEGIAN (e.g. "Hei", "Hallo", "Hvem...")
            - REPLY IN NORWEGIAN.
            - Use institution name: "Høgskolen i Molde".
            - If greeting ("Hei"): "Hei! Velkommen til Høgskolen i Molde. Hva kan jeg hjelpe deg med?"

            CASE 2: User speaks ENGLISH (e.g. "Hi", "Hello", "Who...")
            - REPLY IN ENGLISH.
            - Use institution name: "Molde University College".
            - If greeting ("Hi"): "Hi! Welcome to Molde University College. How can I help you?"
            ---

            USER QUERY: "{query}"

            YOUR TASK:
            Identify the language of the query above and choose the matching response from CASE 1 or CASE 2.
            If it is a general question, answer it in the detected language.
            
            CRITICAL: If you cannot answer the question (e.g. it is not about the university and not a greeting), politely state you don't know and provide this link: [Contact Us](https://www.himolde.no/kontakt-oss/)
            """
        else:
            # Prepend URL to each chunk so the LLM knows the source link for every piece of information.
            # This allows it to generate clickable links for "General Pages" or "Student Life" items.
            context_text = "\n\n".join([
                f"Source: {chunk.get('url', 'Unknown')}\nContent: {chunk.get('content', '')}" 
                for chunk in context_chunks
            ])
            
            prompt_text = settings.RAG_SYSTEM_PROMPT.format(
                context_text=context_text,
                query=query
            )

        url = f"{self.base_url}/{self.generation_model}:generateContent?key={self.api_key}"
        logger.info(f"Generating answer with model: {self.generation_model}")
        # logger.info(f"Prompt preview: {prompt_text[:500]}...") 
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt_text}]
            }]
        }

        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        
        # logger.info(f"Raw Gemini Response: {data}")
        
        if "candidates" not in data or not data["candidates"]:
             logger.error(f"Gemini returned no candidates. Safety block? Data: {data}")
             return "I apologize, but I cannot answer that request."

        # Extract text
        # Structure: candidates[0].content.parts[0].text
        return data["candidates"][0]["content"]["parts"][0]["text"]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def detect_ambiguity(self, query: str) -> dict:
        """Check if query is ambiguous using REST API."""
        import requests
        import json
        
        prompt_text = settings.AMBIGUITY_SYSTEM_PROMPT.format(query=query)
        
        url = f"{self.base_url}/{self.generation_model}:generateContent?key={self.api_key}"
        # Request JSON response
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }
        
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        
        text_content = data["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text_content)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def contextualize_query(self, query: str, history: list[ChatMessage]) -> str:
        """Rewrite query to be self-contained using REST API."""
        if not history:
            return query
            
        import requests
        
        history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
        prompt_text = settings.CONTEXTUALIZE_SYSTEM_PROMPT.format(
            history=history_text,
            query=query
        )
        
        url = f"{self.base_url}/{self.generation_model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }
        
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        
        rewritten = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        logger.info(f"Contextualized Query (REST): '{query}' -> '{rewritten}'")
        return rewritten

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
