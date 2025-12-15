import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from services.scraper import ScraperService
from core.config import settings
from supabase import create_client, Client
import time

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

class IngestionService:
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "models/text-embedding-004"
    BATCH_SIZE = 10

    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        self.scraper_service = ScraperService()

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
            
            # Basic improvement: try to split on period or newline if possible within the last 100 chars
            if end < text_len:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point != -1 and break_point > self.CHUNK_SIZE - 200:
                    end = start + break_point + 1
                    chunk = text[start:end]

            chunks.append(chunk)

            # If we reached the end of the text, break
            if end >= text_len:
                break
                
            # Move start forward
            # Ensure we always move forward at least 1 char to avoid infinite loop
            step = max(1, len(chunk) - self.CHUNK_OVERLAP)
            start += step

        return chunks

    @retry(
        retry=retry_if_exception_type(Exception), # Broad catch for Gemini API errors
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=20)
    )
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts using Gemini."""
        if not texts:
            return []
        
        try:
            # Gemini API supports embedding content in batches
            result = genai.embed_content(
                model=self.EMBEDDING_MODEL,
                content=texts,
                task_type="retrieval_document",
                title=None
            )
            # The result keys vary depending on batch or single, but library handles list input -> dict with 'embedding' key which is a list
            # Wait, verify return structure for batch:
            # {'embedding': [[...], [...]]}
            if 'embedding' in result:
                return result['embedding']
            return []
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

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
                self.supabase.table("document_chunks").delete().eq("url", url).execute()
            except Exception as e:
                logger.error(f"Failed to delete existing chunks for {url}: {e}")
                continue

            # 2. Chunking
            chunks = self._chunk_text(content)
            if not chunks:
                continue

            # 3. Embedding and Storage (Batched)
            for i in range(0, len(chunks), self.BATCH_SIZE):
                batch_chunks = chunks[i : i + self.BATCH_SIZE]
                
                try:
                    embeddings = self._generate_embeddings(batch_chunks)
                    
                    rows_to_insert = []
                    for j, chunk_text in enumerate(batch_chunks):
                        if j < len(embeddings):
                            rows_to_insert.append({
                                "url": url,
                                "chunk_index": i + j,
                                "content": chunk_text,
                                "metadata": {"source": "himolde.no", "title": title},
                                "embedding": embeddings[j]
                            })
                    
                    if rows_to_insert:
                        self.supabase.table("document_chunks").insert(rows_to_insert).execute()
                        total_chunks += len(rows_to_insert)
                        
                except Exception as e:
                    logger.error(f"Failed to process batch for {url}: {e}")
            
            logger.info(f"Processed {url}: {len(chunks)} chunks")

        return {"status": "success", "processed_docs": total_docs, "total_chunks": total_chunks}

    def run_full_pipeline(self):
        """Run scraper then ingestion."""
        logger.info("Running full ingestion pipeline...")
        documents = self.scraper_service.scrape_all_programs()
        return self.process_and_store(documents)
