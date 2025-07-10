#   Purpose:
#       sentiment analysis routes




# ------------------------------------------
# 1. Imports
# ------------------------------------------
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml_models.sentiment_model import predict_sentiment
from transformers import pipeline

router = APIRouter()

classifier = pipeline("sentiment-analysis")



# ------------------------------------------
# 2. request schema
# ------------------------------------------
class SentimentRequest(BaseModel):
    text: str



# ------------------------------------------
# 3. response schema
# ------------------------------------------
class SentimentResponse(BaseModel):
    sentiment: str
    score: float

@router.post("/", response_model=SentimentResponse)
async def get_sentiment(data: SentimentRequest):
    try:
        result = classifier(data.text)[0]
        return SentimentResponse(sentiment=result["label"], score=result["score"])
    except Exception as e:
        print("SENTIMENT ERROR:", e)
        raise
