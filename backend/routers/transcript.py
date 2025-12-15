
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from backend.core.config import settings
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.routers.feedback import submit_feedback, FeedbackRequest, get_supabase

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    role: str
    content: str

class TranscriptRequest(BaseModel):
    email: Optional[EmailStr] = None
    chat_history: List[ChatMessage]
    # Optional Feedback (can be submitted together)
    rating: Optional[int] = Field(None, ge=1, le=10)
    comment: Optional[str] = None

@router.post("/transcript")
async def send_transcript(request: TranscriptRequest, supabase=Depends(get_supabase)):
    """
    Features:
    1. If rating/comment provided, saves feedback to DB.
    2. If email provided, sends chat transcript.
    """
    
    # 1. Handle Feedback if present
    if request.rating:
        try:
            fb_req = FeedbackRequest(
                score=request.rating, # Map back to score/rating alias
                comment=request.comment,
                chat_id=None # We don't have a rigid chat ID in this flow yet
            )
            # Re-use existing feedback logic (or direct insert)
            data = {
                "rating": fb_req.score,
                "comment": fb_req.comment,
                # "term": "Transcript Flow" # Column does not exist in DB
            }
            supabase.table("feedback").insert(data).execute()
        except Exception as e:
            logger.error(f"Feedback save failed in transcript flow: {e}")
            # Continue to email, don't block

    # 2. Handle Email
    if not request.email:
        return {"status": "success", "message": "Feedback saved (no email provided)"}
        
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured. Skipping email send.")
        return {"status": "warning", "message": "Feedback saved, but email service is not configured."}

    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SENDER_EMAIL
        msg['To'] = request.email
        msg['Subject'] = "Your Chat Transcript from Molde University College"

        # Format Body
        body_lines = ["Here is the transcript of your conversation:\n"]
        for msg_item in request.chat_history:
            role = "You" if msg_item.role == "user" else "Assistant"
            body_lines.append(f"**{role}**:\n{msg_item.content}\n")
        
        body_lines.append("\nThank you for chatting with us!")
        
        msg.attach(MIMEText("\n".join(body_lines), 'plain'))

        # Send
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
            
        return {"status": "success", "message": f"Transcript sent to {request.email}"}

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email transcript")
