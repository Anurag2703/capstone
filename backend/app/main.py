# Purpose:
#   1. starts the FastAPI app
#   2. wires up the routers
#   3. sets a simple root route



# ------------------------------------------
# 1. Imports
# ------------------------------------------

# standard library imports
from fastapi import FastAPI
from app.api import routes_healthcheck, routes_burnout, routes_sentiment, routes_chatbot, routes_gita
from fastapi.middleware.cors import CORSMiddleware

# 👇 One-time schema creator
from app.db.models import Base
from app.core.config import engine
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Proactive Mental Wellness Assistant")


# Allow your frontend origin (localhost:5173)
# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------
# 2. include routersImports
# ------------------------------------------
app.include_router(routes_healthcheck.router, prefix="/health")
app.include_router(routes_burnout.router, prefix="/burnout")
app.include_router(routes_sentiment.router, prefix="/sentiment")
app.include_router(routes_chatbot.router, prefix="/chatbot")
app.include_router(routes_gita.router, prefix="/gita")

# optional: root route
@app.get("/")
async def root():
    return {"message": "Mental Wellness Assistant Backend is running."}




# TEMPORARY: for local testing
import logging

logging.basicConfig(level=logging.DEBUG)
