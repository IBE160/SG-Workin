from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional
import logging
from backend.services.scraper import ScraperService
from backend.services.ingestion import IngestionService
from backend.core.config import settings
from supabase import create_client, Client
from backend.dependencies import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)

logger = logging.getLogger(__name__)

# ... existing code ...


@router.delete("/users/{user_id}")
def delete_user_endpoint(user_id: str):
    """Delete a user."""
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        supabase.auth.admin.delete_user(user_id)
        return {"status": "success", "message": f"User {user_id} deleted"}
    except Exception as e:
        logger.error(f"Delete user failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ResetPasswordRequest(BaseModel):
    email: str

@router.post("/users/reset-password")
def reset_password(request: ResetPasswordRequest):
    """Trigger password reset email."""
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        # Generate link or send email. For admin force reset, we often use invite or reset.
        # supabase.auth.admin.invite_user_by_email(email) sends invite.
        # supabase.auth.reset_password_for_email(email) sends reset.
        # Since this is admin panel, reset_password_for_email is good.
        # Note: This usually requires Supabase Email settings to be configured.
        
        # But wait, admin.reset_password_for_email might not exist on Admin API cleanly without link?
        # Let's check Supabase Py/GoTrue.
        # Usually: client.auth.reset_password_for_email(email) 
        # But we are admin. We can generate a link: client.auth.admin.generate_link(...)
        
        # Let's use simple reset trigger if available OR generate link.
        # Safe bet: generate_link(type="recovery", email=...) and return it (or log it/send it).
        # Actually, user wants "Button to trigger password reset email".
        # Standard client sdk: supabase.auth.reset_password_for_email(email, redirect_to=...) 
        # Since we have service role, we can also use that.
        
        response = supabase.auth.reset_password_email(request.email)
        return {"status": "success", "message": f"Password reset email sent to {request.email}"}
        
    except Exception as e:
        logger.error(f"Reset password failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

logger = logging.getLogger(__name__)

class ScrapeRequest(BaseModel):
    url: HttpUrl

    @validator("url")
    def validate_himolde_url(cls, v):
        str_url = str(v)
        if "himolde.no" not in str_url:
            raise ValueError("Only himolde.no URLs are allowed")
        return v

@router.post("/scrape")
def trigger_scrape(request: ScrapeRequest):
    """
    Trigger scraping for a specific URL.
    """
    url_str = str(request.url)
    logger.info(f"Admin triggered scrape for: {url_str}")
    
    try:
        # initialize services
        scraper = ScraperService()
        ingestion = IngestionService()
        
        # 1. Scrape
        documents = scraper.scrape_url(url_str)
        if not documents:
            raise HTTPException(status_code=400, detail="Failed to scrape content from URL")
            
        # 2. Ingest
        result = ingestion.process_and_store(documents)
        
        return {
            "status": "success", 
            "message": "Scraping and ingestion triggered",
            "details": result
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Scrape failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/urls")
def list_scraped_urls():
    """
    List all URLs that have been scraped and stored.
    Uses 'document_chunks' table.
    """
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        
        # Fetch distinct URLs via a simplified query approach
        # Note: Supabase JS/Py doesn't support .distinct() directly in a simple way often without RPC
        # But we can select url from document_chunks.
        # For performance on large datasets this should be an RPC, but for MVP:
        
        # Strategy: Fetch all distinct URLs.
        # Since 'select distinct' is tricky in pure postgrest-py without rpc, 
        # we will use the existing rpc or raw sql if possible, OR just fetch valid chunks.
        # 
        # Better: Create a Postgres function `get_distinct_urls`.
        # Fallback for Agent without SQL access: Fetch a limit of rows and dedup in python (BAD for scale).
        # 
        # Let's try to fetch with .csv() or similar? No.
        # 
        # Let's use a known RPC or just query.
        # Actually, let's just query metadata if possible? 
        # 
        # Plan B: Just fetch all chunks (limit 1000) and dedup in Python (Temporary MVP).
        # OR: Use a hack: .select("url, title, metadata")
        
        # Query without order for safety, and just get active chunks
        # 'title' column does not exist, it's in metadata.
        response = supabase.table("document_chunks").select("url, metadata").execute()
        
        logger.info(f"Admin: Fetched {len(response.data)} chunks from DB")
        
        # Manual Distinct in Python (MVP)
        seen = set()
        unique_urls = []
        
        for row in response.data:
            u = row.get("url")
            if u and u not in seen:
                seen.add(u)
                unique_urls.append({
                    "url": u,
                    "title": row.get("metadata", {}).get("title") or "Untitled",
                    "scraped_at": row.get("metadata", {}).get("scraped_at")
                })
                
        return unique_urls

    except Exception as e:
        logger.error(f"Failed to list URLs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/urls")
def delete_url(url: str):
    """
    Delete all chunks associated with a specific URL.
    """
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        
        # Verify URL exists (optional, but good practice)
        # Delete all chunks with this URL
        response = supabase.table("document_chunks").delete().eq("url", url).execute()
        
        return {"status": "success", "message": f"Deleted content for {url}"}

    except Exception as e:
        logger.error(f"Failed to delete URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/scrape/all")
def delete_all_scraped_data():
    """
    Delete ALL scraped data from document_chunks.
    """
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        
        # Delete all rows. In Supabase/PostgREST, we need a filter to delete.
        # We can use id > 0 or similar if id is int, or something that matches all.
        # 'neq' on a non-null column is a standard way. 'url' is unlikely to be null/empty string if validated.
        
        response = supabase.table("document_chunks").delete().neq("url", "impossible_string_marker").execute()
        
        return {"status": "success", "message": "All scraped data deleted"}

    except Exception as e:
        logger.error(f"Failed to delete all data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class UserCreate(BaseModel):
    email: str
    password: str

@router.get("/users")
def list_users():
    """List all users via Supabase Admin API."""
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        response = supabase.auth.admin.list_users()
        users = response.users if hasattr(response, "users") else response
        return users
    except Exception as e:
        logger.error(f"List users failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users")
def create_user_endpoint(user: UserCreate):
    """Create a new user."""
    try:
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        response = supabase.auth.admin.create_user({
            "email": user.email,
            "password": user.password,
            "email_confirm": True
        })
        return {"user_id": response.user.id, "email": response.user.email}
    except Exception as e:
        logger.error(f"Create user failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


