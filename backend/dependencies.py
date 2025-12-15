
from fastapi import Header, HTTPException, Depends
from supabase import create_client, Client
from backend.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def get_current_user(authorization: str = Header(None)):
    """
    Verifies the Supabase JWT token from the Authorization header.
    Returns the user object if valid, raises HTTPException otherwise.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        token = authorization.replace("Bearer ", "")
        supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
        
        # Verify token using Supabase Auth
        user = supabase.auth.get_user(token)
        
        if not user:
             raise HTTPException(status_code=401, detail="Invalid token")
             
        return user

    except Exception as e:
        logger.error(f"Auth verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
