from fastapi import APIRouter, HTTPException, status
from backend.schemas.feedback import FeedbackCreate
from backend.core.config import settings
from supabase import create_client, Client
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Supabase client
# Ideally this should be a singleton dependency, but following pattern from other services/routers
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(feedback: FeedbackCreate):
    """
    Submit user feedback (rating 1-10 and optional comment).
    """
    try:
        data = {
            "rating": feedback.rating,
            "comment": feedback.comment
        }
        
        # Use service role key to insert into feedback table (bypass RLS if needed, or rely on RLS policy)
        response = supabase.table("feedback").insert(data).execute()
        
        logger.info(f"Feedback submitted: {feedback.rating}")
        return {"status": "success", "message": "Feedback received"}
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )
