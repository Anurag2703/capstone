#   Purpose:
#       This helper gets the database session for use in API endpoints cleanly.


from app.core.config import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()