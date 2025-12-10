from fastapi import APIRouter
from pydantic import BaseModel
from core.constants import WELCOME_MESSAGE

router = APIRouter()

class MessageRequest(BaseModel):
    message: str

@router.post("/messages")
async def send_message(request: MessageRequest):
    return {
        "status": "success",
        "data": {
            "response": WELCOME_MESSAGE
        }
    }
