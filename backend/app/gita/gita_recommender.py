#   Purpose:
#       recommends verses based on sentiment




from app.gita.gita_loader import GitaLoader
import pandas as pd
import random

class GitaRecommender:
    def __init__(self, filepath: str):
        self.df = pd.read_excel(filepath, engine='openpyxl')

        # Normalize column names and sentiment values
        self.df.columns = [col.strip().lower() for col in self.df.columns]
        if 'sentiment' not in self.df.columns:
            raise ValueError("Column 'sentiment' not found in Excel.")
        self.df['sentiment'] = self.df['sentiment'].astype(str).str.strip().str.lower()

        print("Gita verses loaded:", len(self.df))
        print("Sentiment examples:", self.df['sentiment'].unique())

    def recommend_by_sentiment(self, sentiment: str):
        sentiment = sentiment.strip().lower()
        print(f"🔍 Requested sentiment: '{sentiment}'")

        filtered = self.df[self.df['sentiment'] == sentiment]

        if not filtered.empty:
            chosen = filtered.sample(n=1).iloc[0]
            return {
                "chapter": int(chosen.get("chapter", 0)),
                "verse_number": int(chosen.get("verse_number", 0)),
                "verse": str(chosen.get("verse", "")).strip()
            }
        else:
            print("No verses found for this sentiment.")
            return {
                "chapter": 0,
                "verse_number": 0,
                "verse": ""
            }