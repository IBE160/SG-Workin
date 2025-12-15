
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class FeedbackRequest(BaseModel):
    score: int = Field(..., ge=1, le=10, alias="rating", description="Satisfaction score 1-10")
    comment: Optional[str] = Field(None, description="Optional text comment")
    chat_id: Optional[str] = Field(None, description="UUID of the chat session")

    class Config:
        populate_by_name = True

class FeedbackResponse(BaseModel):
    status: str
    message: str
    id: Optional[str] = None
