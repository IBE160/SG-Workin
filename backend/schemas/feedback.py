from pydantic import BaseModel, Field, field_validator
from typing import Optional

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=10, description="Rating from 1 to 10")
    comment: Optional[str] = Field(None, description="Optional text comment")
