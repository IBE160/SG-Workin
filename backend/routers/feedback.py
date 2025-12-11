from fastapi import APIRouter, HTTPException, status
from backend.schemas.feedback import FeedbackCreate
from backend.core.config import settings
from sqlalchemy import create_engine, text
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Use direct DB connection to bypass PostgREST schema cache issues
engine = create_engine(settings.DATABASE_URL)

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_feedback(feedback: FeedbackCreate):
    """
    Submit user feedback (rating 1-10 and optional comment).
    """
    try:
        # Use simple synchronous execution for now
        with engine.connect() as connection:
            statement = text("""
                INSERT INTO public.feedback (rating, comment)
                VALUES (:rating, :comment)
            """)
            connection.execute(statement, {"rating": feedback.rating, "comment": feedback.comment})
            connection.commit()
        
        logger.info(f"Feedback submitted: {feedback.rating}")
        return {"status": "success", "message": "Feedback received"}
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback"
        )
