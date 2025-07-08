#   Purpose:
#       LLM / LangGraph conversation routes




# ------------------------------------------
# 1. Imports
# ------------------------------------------

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.ml_models import chatbot_agent
from app.ml_models.chatbot_agent import get_chain
from app.db import models
from app.core.utils import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

chain = get_chain()



# ------------------------------------------
# 2. Request
# ------------------------------------------
class ChatbotRequest(BaseModel):
    student_id: str
    message: str




# ------------------------------------------
# 3. Response
# ------------------------------------------
class ChatbotResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatbotResponse)
async def chatbot_interaction(
    data: ChatbotRequest,
    db: Session = Depends(get_db)
):
    try:
        reply = chatbot_agent.generate_response({
            "input": data.message,
            "student_id": data.student_id
        })

        # Save to DB
        record = models.ConversationLog(
            student_id=data.student_id,
            message=data.message,
            reply=reply
        )
        db.add(record)
        db.commit()

        return ChatbotResponse(reply=reply)
    except Exception as e:
        # print("CHATBOT ROUTE EXCEPTION:", e)
        logger.error(f"CHATBOT ROUTE EXCEPTION: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")