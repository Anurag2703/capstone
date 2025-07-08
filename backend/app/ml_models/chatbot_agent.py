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
        self.input = input
        self.student_id = student_id
        self.history = []
        self.gita_mode = False
        self.escalated = False






# ---------------------------------------------------------------------
# 4. Router
# ---------------------------------------------------------------------
def router(state: ChatState):
    last_message = state.input
    if "suicidal" in last_message.lower():
        state.escalated = True
        return {"next": "escalate"}
    if state.gita_mode:
        return {"next": "gita"}
    if "help" in last_message.lower():
        return {"next": "comfort"}
    return {"next": "motivate"}






# ---------------------------------------------------------------------
# 5. Motivational tool
# ---------------------------------------------------------------------
def motivate(state: ChatState):
    reply = llm.invoke("Please encourage the student with empathy")
    state.history.append(reply.content)
    return {"response": reply.content, "history": state.history}






# ---------------------------------------------------------------------
# 6. Comfort tool
# ---------------------------------------------------------------------
def comfort(state: ChatState):
    reply = llm.invoke("Provide some comforting advice to the student")
    state.history.append(reply.content)
    return {"response": reply.content, "history": state.history}






# ---------------------------------------------------------------------
# 7. Escalate
# ---------------------------------------------------------------------
def escalate(state: ChatState):
    reply = "Your distress is concerning. Please contact the student counselor immediately."
    state.history.append(reply)
    return {"response": reply, "history": state.history}






# ---------------------------------------------------------------------
# 8. Gita tool
# ---------------------------------------------------------------------
gita = GitaRecommender("app/gita/Bhagwad_Gita.xlsx")

def gita_tool(state: ChatState):
    sentiment = "negative"
    verse = gita.recommend_by_sentiment(sentiment)
    reply = f"{verse['verse']} (Chapter {verse['chapter']})"
    state.history.append(reply)
    return {"response": reply, "history": state.history}






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
graph.add_conditional_edges(
    "router", 
    lambda state: state["next"], 
    {"motivate": "motivate", "comfort": "comfort", "escalate": "escalate", "gita": "gita"}
)

graph.set_entry_point("motivate")
graph.set_finish_point("escalate")  # optional if END not used
compiled_chain = graph.compile()






# ---------------------------------------------------------------------
# 10. wrapper to plug into your FastAPI route
# ---------------------------------------------------------------------
def generate_response(message: str, student_id: str):
    state = ChatState(input=message, student_id=student_id)
    result = compiled_chain.invoke(state)

    if isinstance(result, dict) and "response" in result:
        return result["response"]
    elif hasattr(result, 'response'):
        return result.response
    else:
        return "Sorry, I could not understand."

def get_chain():
    return compiled_chain
