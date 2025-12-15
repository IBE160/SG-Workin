
from fastapi import APIRouter, HTTPException, Depends
from backend.schemas.feedback import FeedbackRequest, FeedbackResponse
from backend.core.config import settings
from supabase import create_client, Client
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize Supabase Client
def get_supabase() -> Client:
    try:
        # Use Service Role Key to bypass RLS for inserts
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest, supabase: Client = Depends(get_supabase)):
    """
    Submit user satisfaction feedback (score 1-10 + comment).
    """
    try:
        data = {
            "rating": feedback.score, # Pydantic model has 'score', map to DB 'rating'
            "comment": feedback.comment,
            "chat_id": feedback.chat_id
        }
        
        # Insert into 'feedback' table
        response = supabase.table("feedback").insert(data).execute()
        
        # Check if insert was successful (response.data should be a list with the inserted row)
        if hasattr(response, 'data') and response.data:
            inserted_id = response.data[0].get('id')
            return FeedbackResponse(
                status="success", 
                message="Feedback received", 
                id=inserted_id
            )
        else:
             # If response format implies using .data directly in older clients
             # Adjust based on library version. 
             # Assuming standard supabase-py behavior.
             return FeedbackResponse(status="success", message="Feedback received (no id returned)")

    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))
