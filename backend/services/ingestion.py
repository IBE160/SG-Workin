import requests
from typing import List, Dict, Any, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from backend.services.scraper import ScraperService
from backend.core.config import settings
from supabase import create_client, Client
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class IngestionService:
    CHUNK_SIZE = 5000 # User requested 5000 chars (~1250 tokens)
    CHUNK_OVERLAP = 1000 # 20% overlap
    EMBEDDING_MODEL = "models/text-embedding-004"
    BATCH_SIZE = 10
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        self.scraper_service = ScraperService()
        self.api_key = settings.GOOGLE_API_KEY

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap."""
        if not text:
            return []
        
        chunks = []
        if len(text) <= self.CHUNK_SIZE:
            return [text]

        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.CHUNK_SIZE
            chunk = text[start:end]
            
            # Basic improvement: try to split on period or newline
            if end < text_len:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point != -1 and break_point > self.CHUNK_SIZE - 200:
                    end = start + break_point + 1
                    chunk = text[start:end]

            chunks.append(chunk)

            if end >= text_len:
                break
                
            step = max(1, len(chunk) - self.CHUNK_OVERLAP)
            start += step

        return chunks

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts using Gemini REST API."""
        if not texts:
            return []
        
        embeddings = []
        for text in texts:
            try:
                # Standard Gemini Embedding
                url = f"{self.BASE_URL}/{self.EMBEDDING_MODEL}:embedContent?key={self.api_key}"
                payload = {
                    "content": {"parts": [{"text": text}]},
                    "taskType": "RETRIEVAL_DOCUMENT"
                }
                
                resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
                resp.raise_for_status()
                data = resp.json()
                
                if "embedding" in data:
                    vec = data["embedding"].get("values")
                    if vec:
                        embeddings.append(vec)
                    else:
                        logger.error(f"No vector found in response: {data}")
                        embeddings.append([])
                else:
                    logger.error(f"Unexpected response: {data}")
                    embeddings.append([])

            except Exception as e:
                logger.error(f"Gemini API error for text chunk: {e}")
                raise e
                
        return embeddings

    def process_and_store(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process documents: chunk, embed, and store in Supabase."""
        total_chunks = 0
        total_docs = len(documents)
        logger.info(f"Starting ingestion for {total_docs} documents")

        for doc in documents:
            url = doc.get("url")
            content = doc.get("content")
            title = doc.get("title")
            
            if not url or not content:
                continue

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def _delete_existing_chunks(self, url: str):
        """Delete existing chunks with retry."""
        self.supabase.table("document_chunks").delete().eq("url", url).execute()

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def _insert_chunks(self, rows: List[Dict]):
        """Insert chunks with retry."""
        self.supabase.table("document_chunks").insert(rows).execute()

    def process_and_store(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process documents: chunk, embed, and store in Supabase."""
        total_chunks = 0
        total_docs = len(documents)
        logger.info(f"Starting ingestion for {total_docs} documents")

        for doc in documents:
            url = doc.get("url")
            content = doc.get("content")
            title = doc.get("title")
            
            if not url or not content:
                continue

            # 1. Idempotency: Remove existing chunks for this URL
            try:
                self._delete_existing_chunks(url)
            except Exception as e:
                logger.error(f"Failed to delete existing chunks for {url} after retries: {e}")
                continue

            # 2. Chunking
            chunks = self._chunk_text(content)
            if not chunks:
                continue
                
            # Prepend Context (Title) to each chunk for better retrieval
            # This ensures that split chunks (like course tables) are still associated with the main topic
            if title:
                chunks = [f"{title}\n\n{c}" for c in chunks]

            # 3. Embedding and Storage (Batched)
            for i in range(0, len(chunks), self.BATCH_SIZE):
                batch_chunks = chunks[i : i + self.BATCH_SIZE]
                
                try:
                    embeddings = self._generate_embeddings(batch_chunks)
                    
                    # Filter out failures
                    rows_to_insert = []
                    for j, chunk_text in enumerate(batch_chunks):
                        if j < len(embeddings) and embeddings[j]: # Ensure embedding exists
                            rows_to_insert.append({
                                "url": url,
                                "chunk_index": i + j,
                                "content": chunk_text,
                                "metadata": {
                                    "source": "himolde.no", 
                                    "title": title,
                                    "scraped_at": datetime.utcnow().isoformat()
                                },
                                "embedding": embeddings[j]
                            })
                    
                    if rows_to_insert:
                        self._insert_chunks(rows_to_insert)
                        total_chunks += len(rows_to_insert)
                        
                except Exception as e:
                    logger.error(f"Failed to process batch for {url}: {e}")
            
            logger.info(f"Processed {url}: {len(chunks)} chunks")

        return {"status": "success", "processed_docs": total_docs, "total_chunks": total_chunks}

    def run_full_pipeline(self):
        """Run scraper then ingestion."""
        logger.info("Running full ingestion pipeline...")
        documents = self.scraper_service.scrape_everything()
        return self.process_and_store(documents)
