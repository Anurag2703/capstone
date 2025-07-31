# -----------------------------------------
# Imports
# -----------------------------------------
import json
import random
from transformers import pipeline



# -----------------------------------------
# Load HuggingFace sentiment model
# -----------------------------------------
sentiment_pipeline = pipeline("sentiment-analysis")



# -----------------------------------------
# Grouped distress keywords by theme
# -----------------------------------------
DISTRESS_KEYWORDS = {
    "suicidal": [
        "suicidal", "suicide", "kill myself", "i want to die",
        "end it all", "i want to end it", "ending my life",
        "wish i wasn’t born", "i want to sleep forever"
    ],
    "hopeless": [
        "hopeless", "no way out", "i give up", "i'm done",
        "nothing matters anymore", "life is meaningless",
        "lost all hope", "feel empty", "no purpose", "done with life"
    ],
    "self_harm": [
        "hurting myself", "self harm", "cutting myself", "i hate myself",
        "i'm not enough", "i feel trapped"
    ],
    "depression": [
        "depressed", "depression", "crying every day", "i’m tired of everything",
        "dying inside", "dark thoughts", "alone and broken", "feeling shattered",
        "too much pain", "my life is a mess", "exhausted mentally"
    ],
    "anxiety": [
        "anxious all the time", "panic attack", "can’t breathe", "overwhelmed",
        "can’t take it anymore", "nobody understands me", "no one cares"
    ]
}



# -----------------------------------------
# Load response variations per theme
# -----------------------------------------
with open("app/responses/theme_responses.json", "r", encoding="utf-8") as f:
    THEME_RESPONSES = json.load(f)



# -----------------------------------------
# Load categorized prompt examples (prompt training base)
# -----------------------------------------
with open("app/responses/prompts_by_emotion.json", "r", encoding="utf-8") as f:
    PROMPT_EXAMPLES = json.load(f)

# Merge prompt examples into DISTRESS_KEYWORDS
for emotion, examples in PROMPT_EXAMPLES.items():
    if emotion in DISTRESS_KEYWORDS:
        DISTRESS_KEYWORDS[emotion].extend([msg.lower() for msg in examples])
    else:
        DISTRESS_KEYWORDS[emotion] = [msg.lower() for msg in examples]



# -----------------------------------------
# Memory to track last used responses
# -----------------------------------------
USED_RESPONSES = {theme: set() for theme in THEME_RESPONSES}

def is_distress_message(message: str) -> tuple[bool, str | None]:
    message = message.lower()

    for theme, keywords in DISTRESS_KEYWORDS.items():
        if any(phrase in message for phrase in keywords):
            return True, theme

    prediction = sentiment_pipeline(message[:512])[0]
    if prediction["label"] == "NEGATIVE" and prediction["score"] > 0.9:
        return True, "negative"

    return False, None



# -----------------------------------------
# Function: get_theme_response()
# -----------------------------------------
def get_theme_response(theme: str) -> str:
    if theme not in THEME_RESPONSES:
        return "Take care. You're not alone."

    unused = list(set(THEME_RESPONSES[theme]) - USED_RESPONSES[theme])
    if not unused:
        USED_RESPONSES[theme].clear()
        unused = THEME_RESPONSES[theme]
    selected = random.choice(unused)
    USED_RESPONSES[theme].add(selected)
    return selected


# -----------------------------------------
# Function: Keyword-based burnout detector
# -----------------------------------------
burnout_keywords = [
    "burnout", "exhausted", "tired", "overwhelmed", "no motivation",
    "too much pressure", "mentally drained", "can't focus", "fatigued",
    "stressed", "always tired", "academic pressure", "losing interest"
]

def detect_burnout_keywords(message: str) -> bool:
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in burnout_keywords)
