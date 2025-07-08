#   Purpose:
#       1. mood tracking, burnout risk, conversation logs, and optional Gita invocations
#       2. Contains tables for:
#               - StudentMoodLog → stores daily/weekly mood check-ins
#               - BurnoutRiskLog → stores every burnout risk prediction
#               - ConversationLog → logs every message + reply for analytics
#               - GitaModeLog → tracks if/when the user opted into Gita support




# ------------------------------------------
# 1. Imports
# ------------------------------------------
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
datetime.now(timezone.utc)

Base = declarative_base()



# -------------------------------------------------------------------------------
# 2. StudentMoodLog → stores daily/weekly mood check-ins
# -------------------------------------------------------------------------------
class StudentMoodLog(Base):
    __tablename__ = "student_mood_logs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    mood = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)



# -------------------------------------------------------------------------------
# 3. BurnoutRiskLog → stores every burnout risk prediction
# -------------------------------------------------------------------------------
class BurnoutRiskLog(Base):
    __tablename__ = "burnout_risk_logs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    risk_score = Column(Float)
    risk_level = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)



# -------------------------------------------------------------------------------
# 4. ConversationLog → logs every message + reply for analytics
# -------------------------------------------------------------------------------
class ConversationLog(Base):
    __tablename__ = "conversation_logs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    message = Column(Text)
    reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)



# -------------------------------------------------------------------------------
# 5. GitaModeLog → tracks if/when the user opted into Gita support
# -------------------------------------------------------------------------------
class GitaModeLog(Base):
    __tablename__ = "gita_mode_logs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    activated = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
