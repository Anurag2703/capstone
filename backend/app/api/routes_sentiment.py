#   Purpose:
#       sentiment analysis routes




# ------------------------------------------
# 1. Imports
# ------------------------------------------
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml_models.sentiment_model import predict_sentiment

router = APIRouter()



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
async def analyze_sentiment(data: SentimentRequest):
    try:
        sentiment = predict_sentiment(data.text)
        return SentimentResponse(sentiment=sentiment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
