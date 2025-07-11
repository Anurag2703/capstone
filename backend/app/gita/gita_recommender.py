#   Purpose:
#       recommends verses based on sentiment




import json
import pandas as pd

class GitaRecommender:
    def __init__(self, filepath: str):
        self.df = pd.read_excel(filepath, engine="openpyxl")
        self.df.columns = [col.strip().lower().replace(" ", "_") for col in self.df.columns]

        # Force chapter and verse to integer type
        self.df["chapter"] = self.df["chapter"].astype(int)
        self.df["verse"] = self.df["verse"].astype(int)

        # Load sentiment map from JSON
        with open("app/gita/sentiment_map.json", "r", encoding="utf-8") as f:
            self.sentiment_map = json.load(f)

    def recommend_by_sentiment(self, sentiment: str):
        sentiment = sentiment.strip().lower()

        if sentiment not in self.sentiment_map:
            return {"verse": "", "chapter": 0, "verse_number": 0}

        # Ensure chapter and verse columns are integers for matching
        self.df["chapter"] = self.df["chapter"].astype(int)
        self.df["verse"] = self.df["verse"].astype(int)

        print(f"Matching sentiment: '{sentiment}' → verses: {self.sentiment_map[sentiment]}")
        print(f"Available columns: {self.df.columns.tolist()}")
        print(self.df[['chapter', 'verse']].head())

        
        # Look for first matching verse in the dataframe
        for chapter, verse in self.sentiment_map[sentiment]:
            print(f"Trying to match Chapter={chapter}, Verse={verse}")
            match = self.df[
                (self.df["chapter"] == chapter) &
                (self.df["verse"] == verse)
            ]
            if not match.empty:
                row = match.iloc[0]
                return {
                    "verse": row.get("shloka") or row.get("engmeaning", ""),
                    "chapter": chapter,
                    "verse_number": verse,
                    "sentiment": sentiment
                }
            else:
                print(f"No match found for Chapter={chapter}, Verse={verse}")


        return {"verse": "", "chapter": 0, "verse_number": 0}


        # for chapter, verse in self.sentiment_map[sentiment]:
        #     match = self.df[
        #         (self.df["chapter"] == chapter) &
        #         (self.df["verse"] == verse)
        #     ]
        #     if not match.empty:
        #         row = match.iloc[0]
        #         return {
        #             "verse": row.get("shloka") or row.get("engmeaning", ""),
        #             "chapter": chapter,
        #             "verse_number": verse,
        #             "sentiment": sentiment
        #         }