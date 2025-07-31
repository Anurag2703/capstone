# Purpose:
#   LLM / LangGraph conversation routes

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
import random
import pandas as pd

logger = logging.getLogger(__name__)
router = APIRouter()

chain = get_chain()

# Load Gita data for fallback use
GITA_FILE_PATH = "app/gita/Bhagwad_Gita_with_Sentiment.xlsx"
gita_df = pd.read_excel(GITA_FILE_PATH)

def get_random_shloka():
    random_row = gita_df.sample(1).iloc[0]
    return f"Chapter {random_row['Chapter']}, Verse {random_row['Verse']}:\n{random_row['Shloka']}"

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
        print("Received request:", data.dict())  # ✅ Debugging

        try:
            # expects: { response, proverb, shloka, emotion, gita_mode, escalated }
            result = chatbot_agent.generate_response(data.message, data.student_id)
            print("Generated result:", result)  # ✅ Debugging
        except Exception as e:
            logger.exception("Chatbot failed to generate response")
            fallback = "⚠️ Sorry, I'm having trouble responding right now. Please try again in a while.\n\n🕉️ Be calm and seek help. You are not alone."
            return ChatbotResponse(reply=fallback)

        # Log to DB
        record = models.ConversationLog(
            student_id=data.student_id,
            message=data.message,
            reply=result["response"],
            escalated=result.get("escalated", False),
            gita_mode=result.get("gita_mode", False),
            emotion=result.get("emotion", "unknown")
        )
        db.add(record)
        db.commit()
        print("DB commit successful")  # ✅ Debugging

        # Use fallback if shloka is None
        shloka = result.get("shloka") or get_random_shloka()

        full_reply = (
            f"{result['response']}\n\n"
            f"💡 *Proverb*: {result.get('proverb', '—')}\n"
            f"🕉️ *Gita Shloka*: {shloka}"
        )

        return ChatbotResponse(reply=full_reply)

    except Exception as e:
        logger.exception("CHATBOT ROUTE EXCEPTION")
        raise HTTPException(status_code=500, detail="Something went wrong in the chatbot interaction.")











# # ------------------------------------------
# # 1. Imports
# # ------------------------------------------
# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from pydantic import BaseModel
# from app.ml_models import chatbot_agent
# from app.ml_models.chatbot_agent import get_chain
# from app.db import models
# from app.core.utils import get_db
# import logging
# import random
# import pandas as pd

# logger = logging.getLogger(__name__)
# router = APIRouter()

# chain = get_chain()

# # Load Gita data for fallback use
# GITA_FILE_PATH = "app/gita/Bhagwad_Gita_with_Sentiment.xlsx"
# gita_df = pd.read_excel(GITA_FILE_PATH)

# def get_random_shloka():
#     random_row = gita_df.sample(1).iloc[0]
#     return f"Chapter {random_row['Chapter']}, Verse {random_row['Verse']}:\n{random_row['Shloka']}"





# # ------------------------------------------
# # 2. Request
# # ------------------------------------------
# class ChatbotRequest(BaseModel):
#     student_id: str
#     message: str





# # ------------------------------------------
# # 3. Response
# # ------------------------------------------
# class ChatbotResponse(BaseModel):
#     reply: str

# @router.post("/", response_model=ChatbotResponse)
# async def chatbot_interaction(
#     data: ChatbotRequest,
#     db: Session = Depends(get_db)
# ):
#     try:
#         print("Received request:", data.dict())  # ✅ Debugging

#         # expects: { response, proverb, shloka, emotion, gita_mode, escalated }
#         result = chatbot_agent.generate_response(data.message, data.student_id)
#         print("Generated result:", result)  # ✅ Debugging

#         # Log to DB
#         record = models.ConversationLog(
#             student_id=data.student_id,
#             message=data.message,
#             reply=result["response"],
#             escalated=result.get("escalated", False),
#             gita_mode=result.get("gita_mode", False),
#             emotion=result.get("emotion", "unknown")
#         )
#         db.add(record)
#         db.commit()
#         print("DB commit successful")  # ✅ Debugging

#         # Use fallback if shloka is None
#         shloka = result.get("shloka") or get_random_shloka()

#         full_reply = (
#             f"{result['response']}\n\n"
#             f"💡 *Proverb*: {result.get('proverb', '—')}\n"
#             f"🕉️ *Gita Shloka*: {shloka}"
#         )

#         return ChatbotResponse(reply=full_reply)

#     except Exception as e:
#         logger.exception("CHATBOT ROUTE EXCEPTION")
#         raise HTTPException(status_code=500, detail=str(e))
