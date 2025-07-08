#   Purpose:
#       recommends verses based on sentiment




from app.gita.gita_loader import GitaLoader
import random

class GitaRecommender:
    def __init__(self, filepath: str):
        self.loader = GitaLoader(filepath)
        self.verses = self.loader.get_all_verses()

    def recommend_by_sentiment(self, sentiment: str):
        """
            naive rule-based match:
                - negative sentiment → verses on courage
                - positive sentiment → verses on duty
                - neutral → random
        """

        if sentiment == "negative":
            candidates = [
                verse for verse in self.verses
                if "courage" in str(verse.get("Shloka", "")).lower()
                or "fearless" in str(verse.get("Shloka", "")).lower()
            ]
        elif sentiment == "positive":
            candidates = [
                verse for verse in self.verses
                if "duty" in str(verse.get("Shloka", "")).lower()
            ]
        else:
            candidates = self.verses


        if candidates:
            return random.choice(candidates)
        else:
            return random.choice(self.verses)
