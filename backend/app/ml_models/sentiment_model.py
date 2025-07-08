#   Purpose:
#       load/predict sentiment





# -----------------------------------------
# 1. Imports.
# -----------------------------------------
from transformers import pipeline




# ----------------------------------------------------------------
# 2. sentiment pipeline
# ----------------------------------------------------------------
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def predict_sentiment(text: str):
    """
    Predicts sentiment from text using a transformer
    """
    result = sentiment_pipeline(text)[0]
    return result["label"].lower()  # positive / negative