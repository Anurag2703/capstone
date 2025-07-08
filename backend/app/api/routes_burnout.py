#   Purpose:
#       burnout detection routes



# ------------------------------------------
# 1. Imports
# ------------------------------------------

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.ml_models import burnout_model
from app.db import models
from app.core.utils import get_db

router = APIRouter()



# ------------------------------------------
# 2. Request model
# ------------------------------------------
class BurnoutRequest(BaseModel):
    student_id: str
    login_frequency: int
    forum_activity: int
    assignment_delay_days: int
    missed_classes: int



# ------------------------------------------
# 3. Response model
# ------------------------------------------
class BurnoutResponse(BaseModel):
    risk_score: float
    risk_level: str

@router.post("/", response_model=BurnoutResponse)
async def predict_burnout(
    data: BurnoutRequest,
    db: Session = Depends(get_db)
):
    try:
        score, risk_level = burnout_model.predict_burnout_risk(
            login_freq=data.login_frequency,
            forum_activity=data.forum_activity,
            assignment_delay=data.assignment_delay_days,
            missed_classes=data.missed_classes
        )

        # This will store every burnout risk prediction automatically in the burnout_risk_logs table.
        record = models.BurnoutRiskLog(
            student_id=data.student_id,
            risk_score=score,
            risk_level=risk_level
        )
        db.add(record)
        db.commit()

        return BurnoutResponse(risk_score=score, risk_level=risk_level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
