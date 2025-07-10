# ---------------------------------------------------------------------
#   chatbot_agent.py
#   Purpose:
#       - Gemini via LangChain
#       - LangGraph as a flexible conversation flow
#       - Gita mode as an optional branch
#       - escalation triggers
#       - all wrapped under the FastAPI routes_chatbot.py
# ---------------------------------------------------------------------






from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from app.gita.gita_recommender import GitaRecommender
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------
# 2. Gemini LLM
# ---------------------------------------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)






# ---------------------------------------------------------------------
# 3. LangGraph State
# ---------------------------------------------------------------------
class ChatState:
    def __init__(self, input: str = "", student_id: str = ""):
        self.history = [input]
        self.gita_mode = False
        self.escalated = False
        self.response = ""
        self.student_id = student_id
        self.emotion = None






# ---------------------------------------------------------------------
# 4. Router
# ---------------------------------------------------------------------
def router(state: ChatState):
    last_message = state.history[-1] if state.history else ""
    if "suicidal" in last_message.lower():
        state.escalated = True
        return "escalate"
    if state.gita_mode:
        return "gita"
    if "help" in last_message.lower():
        return "comfort"
    return "motivate"






# ---------------------------------------------------------------------
# 5. Motivational tool
# ---------------------------------------------------------------------
def motivate(state: ChatState):
    reply = llm.invoke("Please encourage the student with empathy")
    state.response = reply.content
    state.history.append(reply.content)
    return state






# ---------------------------------------------------------------------
# 6. Comfort tool
# ---------------------------------------------------------------------
def comfort(state: ChatState):
    reply = llm.invoke("Provide some comforting advice to the student")
    state.response = reply.content
    state.history.append(reply.content)
    return state






# ---------------------------------------------------------------------
# 7. Escalate
# ---------------------------------------------------------------------
def escalate(state: ChatState):
    reply = "Your distress is concerning. Please contact the student counselor immediately."
    state.response = reply
    state.history.append(reply)
    return state






# ---------------------------------------------------------------------
# 8. Gita tool
# ---------------------------------------------------------------------
gita = GitaRecommender("app/gita/Bhagwad_Gita_with_Sentiment.xlsx")

def gita_tool(state: ChatState):
    sentiment = "negative"
    result = gita.recommend_by_sentiment(sentiment)
    reply = f"{result['verse']} (Chapter {result['chapter']})"
    state.response = reply
    state.emotion = sentiment
    state.history.append(reply)
    return state






# ---------------------------------------------------------------------
# 9. Build the graph
# ---------------------------------------------------------------------
graph = StateGraph(ChatState)

graph.add_node("motivate", motivate)
graph.add_node("comfort", comfort)
graph.add_node("escalate", escalate)
graph.add_node("gita", gita_tool)
graph.add_node("router", router)

graph.add_edge("motivate", "router")
graph.add_edge("comfort", "router")
graph.add_edge("gita", "router")
graph.add_edge("router", END)
graph.add_edge("escalate", END)

graph.set_entry_point("motivate")
compiled_chain = graph.compile()






# ---------------------------------------------------------------------
# 10. wrapper to plug into your FastAPI route
# ---------------------------------------------------------------------
def generate_response(message: str, student_id: str):
    result = compiled_chain.invoke({"input": message, "student_id": student_id})
    return {
        "response": result.response,
        "escalated": result.escalated,
        "gita_mode": result.gita_mode,
        "emotion": getattr(result, "emotion", None)
    }


def get_chain():
    return compiled_chain
