import os
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from app.gita.gita_recommender import GitaRecommender
from .sentiment_utils import is_distress_message, get_theme_response

load_dotenv()

# Load Gita DataFrame for sentiment-based lookup
GITA_DF = pd.read_excel("app/gita/Bhagwad_Gita_with_Sentiment.xlsx")

# -----------------------------------------
# 1. LLM Setup
# -----------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)

# -----------------------------------------
# 2. Chat State
# -----------------------------------------
class ChatState:
    def __init__(self, input="", student_id=""):
        self.history = [input]
        self.gita_mode = False
        self.escalated = False
        self.response = ""
        self.student_id = student_id
        self.emotion = None
        self.proverb = "This too shall pass."
        self.shloka = ""
        self.next = "chat"

    def to_dict(self):
        return {
            "history": self.history,
            "gita_mode": self.gita_mode,
            "escalated": self.escalated,
            "response": self.response,
            "student_id": self.student_id,
            "emotion": self.emotion,
            "proverb": self.proverb,
            "shloka": self.shloka,
            "next": self.next
        }

    @classmethod
    def from_dict(cls, data):
        state = cls()
        state.history = data.get("history", [])
        state.gita_mode = data.get("gita_mode", False)
        state.escalated = data.get("escalated", False)
        state.response = data.get("response", "")
        state.student_id = data.get("student_id", "")
        state.emotion = data.get("emotion")
        state.proverb = data.get("proverb", "This too shall pass.")
        state.shloka = data.get("shloka", "")
        state.next = data.get("next", "chat")
        return state

# -----------------------------------------
# 3. Gita Recommender
# -----------------------------------------
gita = GitaRecommender("app/gita/Bhagwad_Gita_with_Sentiment.xlsx")

# -----------------------------------------
# 4. Utility
# -----------------------------------------
def ensure_state(state_dict):
    return state_dict if isinstance(state_dict, ChatState) else ChatState.from_dict(state_dict)

# -----------------------------------------
# 5. Sloka Selector
# -----------------------------------------
def get_random_gita_sloka_by_sentiment(sentiment="negative"):
    sentiment = sentiment.lower().strip()
    try:
        filtered = GITA_DF[GITA_DF["sentiment"].str.lower() == sentiment]
        if filtered.empty:
            filtered = GITA_DF[GITA_DF["sentiment"].str.lower().str.contains(sentiment[:4])]
        if filtered.empty:
            return "🕉️ Be calm and seek help. You are not alone."

        row = filtered.sample(1).iloc[0]
        return f"""📜 *Sloka (Chapter {row['chapter']}, Verse {row['verse']})*: 
{row['shloka']}

🧠 *Translation*:
{row['engmeaning']}"""
    except Exception as e:
        print("⚠️ Error selecting Gita sloka:", e)
        return "🕉️ Be calm and seek help. You are not alone."

# -----------------------------------------
# 6. Nodes
# -----------------------------------------
def chat(state_dict):
    state = ensure_state(state_dict)
    last_user_input = state.history[-1] if state.history else "Hello"
    if not last_user_input.strip():
        last_user_input = "Hi"
    reply = llm.invoke(last_user_input).content
    state.response = reply
    state.history.append(reply)
    state.next = "router"
    return state.to_dict()

def motivate(state_dict):
    state = ensure_state(state_dict)
    reply = llm.invoke("Please encourage the student with empathy").content
    state.response = reply
    state.history.append(reply)
    state.next = "router"
    return state.to_dict()

def comfort(state_dict):
    state = ensure_state(state_dict)
    reply = llm.invoke("Provide comforting advice to someone who feels anxious").content
    state.response = reply
    state.history.append(reply)
    state.next = "router"
    return state.to_dict()

def escalate(state_dict):
    state = ensure_state(state_dict)
    reply = "Your distress is concerning. Please contact the student counselor immediately."
    state.response = reply
    state.history.append(reply)
    state.next = "end"
    return state.to_dict()

def gita_tool(state_dict):
    state = ensure_state(state_dict)
    sentiment = state.emotion or "negative"
    verse_text = get_random_gita_sloka_by_sentiment(sentiment)
    state.response = verse_text
    state.shloka = verse_text
    state.history.append(verse_text)
    state.next = "router"
    return state.to_dict()

# ------------------------------------------
# 7. Router
# ------------------------------------------
def router(state_dict):
    state = ensure_state(state_dict)
    last_message = state.history[-1] if state.history else ""

    casual_inputs = ["hi", "hey", "hello"]
    normalized = last_message.lower().strip()

    if len(state.history) > 5 or any(greet in normalized for greet in casual_inputs):
        state.next = "end"
    elif "suicidal" in normalized:
        state.escalated = True
        state.next = "escalate"
    elif state.gita_mode:
        state.next = "gita"
    elif any(kw in normalized for kw in ["help", "lost", "what should i do"]):
        state.next = "comfort"
    else:
        state.next = "chat"

    return state.to_dict()



# ------------------------------------------
# 8. Routing logic
# ------------------------------------------
def extract_next_node(state_dict):
    state = ensure_state(state_dict)
    return state.next

# ------------------------------------------
# 9. LangGraph
# ------------------------------------------
graph = StateGraph(ChatState)

graph.add_node("chat", chat)
graph.add_node("motivate", motivate)
graph.add_node("comfort", comfort)
graph.add_node("escalate", escalate)
graph.add_node("gita", gita_tool)
graph.add_node("router", router)
graph.add_node("end", lambda x: x)

graph.set_entry_point("chat")

graph.add_edge("chat", "router")
graph.add_edge("motivate", "router")
graph.add_edge("comfort", "router")
graph.add_edge("gita", "router")
graph.add_edge("escalate", "end")
graph.add_edge("end", END)

graph.add_conditional_edges("router", extract_next_node)

compiled_chain = graph.compile()

# ------------------------------------------
# 10. API wrapper
# ------------------------------------------
def generate_response(message: str, student_id: str):
    is_distress, theme = is_distress_message(message)

    if is_distress:
        theme = theme or "negative"
        response = get_theme_response(theme) + "\n\n"
        sloka = get_random_gita_sloka_by_sentiment(theme)
        response += sloka
        return {
            "response": response,
            "escalated": True,
            "gita_mode": True,
            "emotion": theme,
            "proverb": "This too shall pass.",
            "shloka": sloka
        }

    print("🧪 Sending to compiled_chain:", message, student_id)
    initial_state = ChatState(input=message, student_id=student_id).to_dict()
    result = compiled_chain.invoke(initial_state, config={"recursion_limit": 10})
    print("✅ Response from chain:", result)

    state = ensure_state(result)
    return {
        "response": state.response,
        "escalated": state.escalated,
        "gita_mode": state.gita_mode,
        "emotion": state.emotion,
        "proverb": state.proverb,
        "shloka": state.shloka or "You have the right to perform your prescribed duties..."
    }

def get_chain():
    return compiled_chain










# import os
# import pandas as pd
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.graph import StateGraph, END
# from app.gita.gita_recommender import GitaRecommender
# from .sentiment_utils import is_distress_message, get_theme_response

# load_dotenv()

# # Load Gita DataFrame for sentiment-based lookup
# GITA_DF = pd.read_excel("app/gita/Bhagwad_Gita_with_Sentiment.xlsx")

# # -----------------------------------------
# # 1. LLM Setup
# # -----------------------------------------
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     api_key=os.environ["GEMINI_API_KEY"]
# )

# # -----------------------------------------
# # 2. Chat State
# # -----------------------------------------
# class ChatState:
#     def __init__(self, input="", student_id=""):
#         self.history = [input]
#         self.gita_mode = False
#         self.escalated = False
#         self.response = ""
#         self.student_id = student_id
#         self.emotion = None
#         self.proverb = "This too shall pass."
#         self.shloka = ""
#         self.next = "motivate"

#     def to_dict(self):
#         return {
#             "history": self.history,
#             "gita_mode": self.gita_mode,
#             "escalated": self.escalated,
#             "response": self.response,
#             "student_id": self.student_id,
#             "emotion": self.emotion,
#             "proverb": self.proverb,
#             "shloka": self.shloka,
#             "next": self.next
#         }

#     @classmethod
#     def from_dict(cls, data):
#         state = cls()
#         state.history = data.get("history", [])
#         state.gita_mode = data.get("gita_mode", False)
#         state.escalated = data.get("escalated", False)
#         state.response = data.get("response", "")
#         state.student_id = data.get("student_id", "")
#         state.emotion = data.get("emotion")
#         state.proverb = data.get("proverb", "This too shall pass.")
#         state.shloka = data.get("shloka", "")
#         state.next = data.get("next", "motivate")
#         return state

# # -----------------------------------------
# # 3. Gita Recommender
# # -----------------------------------------
# gita = GitaRecommender("app/gita/Bhagwad_Gita_with_Sentiment.xlsx")

# # -----------------------------------------
# # 4. Utility
# # -----------------------------------------
# def ensure_state(state_dict):
#     return state_dict if isinstance(state_dict, ChatState) else ChatState.from_dict(state_dict)

# # -----------------------------------------
# # 5. Sloka Selector
# # -----------------------------------------
# def get_random_gita_sloka_by_sentiment(sentiment="negative"):
#     sentiment = sentiment.lower().strip()
#     try:
#         filtered = GITA_DF[GITA_DF["sentiment"].str.lower() == sentiment]
#         if filtered.empty:
#             filtered = GITA_DF[GITA_DF["sentiment"].str.lower().str.contains(sentiment[:4])]
#         if filtered.empty:
#             return "🕉️ Be calm and seek help. You are not alone."

#         row = filtered.sample(1).iloc[0]
#         return f"""📜 *Sloka (Chapter {row['chapter']}, Verse {row['verse']})*: 
# {row['shloka']}

# 🧠 *Translation*:
# {row['engmeaning']}"""
#     except Exception as e:
#         print("⚠️ Error selecting Gita sloka:", e)
#         return "🕉️ Be calm and seek help. You are not alone."

# # -----------------------------------------
# # 6. Nodes
# # -----------------------------------------
# def motivate(state_dict):
#     state = ensure_state(state_dict)
#     reply = llm.invoke("Please encourage the student with empathy").content
#     state.response = reply
#     state.history.append(reply)
#     state.next = "router"
#     return state.to_dict()

# def comfort(state_dict):
#     state = ensure_state(state_dict)
#     reply = llm.invoke("Provide comforting advice to someone who feels anxious").content
#     state.response = reply
#     state.history.append(reply)
#     state.next = "router"
#     return state.to_dict()

# def escalate(state_dict):
#     state = ensure_state(state_dict)
#     reply = "Your distress is concerning. Please contact the student counselor immediately."
#     state.response = reply
#     state.history.append(reply)
#     state.next = "end"
#     return state.to_dict()

# def gita_tool(state_dict):
#     state = ensure_state(state_dict)
#     sentiment = state.emotion or "negative"
#     verse_text = get_random_gita_sloka_by_sentiment(sentiment)
#     state.response = verse_text
#     state.shloka = verse_text
#     state.history.append(verse_text)
#     state.next = "router"
#     return state.to_dict()

# # ------------------------------------------
# # 7. Router
# # ------------------------------------------
# def router(state_dict):
#     state = ensure_state(state_dict)
#     last_message = state.history[-1] if state.history else ""

#     if len(state.history) > 5 or len(last_message.strip()) < 3:
#         state.next = "end"
#     elif "suicidal" in last_message.lower():
#         state.escalated = True
#         state.next = "escalate"
#     elif state.gita_mode:
#         state.next = "gita"
#     elif any(kw in last_message.lower() for kw in ["help", "lost", "what should i do"]):
#         state.next = "comfort"
#     else:
#         state.next = "motivate"

#     return state.to_dict()

# # ------------------------------------------
# # 8. Routing logic
# # ------------------------------------------
# def extract_next_node(state_dict):
#     state = ensure_state(state_dict)
#     return state.next

# # ------------------------------------------
# # 9. LangGraph
# # ------------------------------------------
# graph = StateGraph(ChatState)

# graph.add_node("motivate", motivate)
# graph.add_node("comfort", comfort)
# graph.add_node("escalate", escalate)
# graph.add_node("gita", gita_tool)
# graph.add_node("router", router)
# graph.add_node("end", lambda x: x)

# graph.set_entry_point("motivate")

# graph.add_edge("motivate", "router")
# graph.add_edge("comfort", "router")
# graph.add_edge("gita", "router")
# graph.add_edge("escalate", "end")
# graph.add_edge("end", END)

# graph.add_conditional_edges("router", extract_next_node)

# compiled_chain = graph.compile()

# # ------------------------------------------
# # 10. API wrapper
# # ------------------------------------------
# def generate_response(message: str, student_id: str):
#     is_distress, theme = is_distress_message(message)

#     if is_distress:
#         theme = theme or "negative"
#         response = get_theme_response(theme) + "\n\n"
#         sloka = get_random_gita_sloka_by_sentiment(theme)
#         response += sloka
#         return {
#             "response": response,
#             "escalated": True,
#             "gita_mode": True,
#             "emotion": theme,
#             "proverb": "This too shall pass.",
#             "shloka": sloka
#         }

#     print("🧪 Sending to compiled_chain:", message, student_id)
#     initial_state = ChatState(input=message, student_id=student_id).to_dict()
#     result = compiled_chain.invoke(initial_state, config={"recursion_limit": 10})
#     print("✅ Response from chain:", result)

#     state = ensure_state(result)
#     return {
#         "response": state.response,
#         "escalated": state.escalated,
#         "gita_mode": state.gita_mode,
#         "emotion": state.emotion,
#         "proverb": state.proverb,
#         "shloka": state.shloka or "You have the right to perform your prescribed duties..."
#     }

# def get_chain():
#     return compiled_chain
