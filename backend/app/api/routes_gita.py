#   Purpose:
#       API endpoint to call recommendations




# ------------------------------------------
# 1. Imports
# ------------------------------------------
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.gita.gita_recommender import GitaRecommender
from app.db import models
from app.core.utils import get_db

router = APIRouter()

# adjust path to match your data location:
GITA_FILE = "app/gita/Bhagwad_Gita_with_Sentiment.xlsx"
recommender = GitaRecommender(GITA_FILE)



# ------------------------------------------
# 2. Request model
# ------------------------------------------
class GitaRequest(BaseModel):
    student_id: str
    sentiment: str



# ------------------------------------------
# 3. Response model
# ------------------------------------------
class GitaResponse(BaseModel):
    chapter: int
    verse_number: int
    verse: str

@router.post("/", response_model=GitaResponse)
async def gita_verse(
    data: GitaRequest,
    db: Session = Depends(get_db)
):  # sourcery skip: raise-from-previous-error
    try:
        recommendation = recommender.recommend_by_sentiment(data.sentiment)

        # log Gita mode activation
        record = models.GitaModeLog(
            student_id=data.student_id,
            activated=True
        )
        db.add(record)
        db.commit()

        return GitaResponse(
            chapter=recommendation.get("Chapter", 0),
            verse_number=recommendation.get("Verse", 0),
            verse=recommendation.get("Shloka", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
