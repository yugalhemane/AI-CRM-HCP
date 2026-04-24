from langgraph.graph import END, StateGraph

from app.tools.log_interaction import log_interaction
from app.tools.edit_interaction import edit_interaction
from app.tools.suggest_action import suggest_action
from app.tools.get_history import get_history
from app.tools.summarize import summarize


# 🧠 Router logic (NOT a node)
def router(state):
    text = state.get("input", "").lower()

    if any(word in text for word in ["change", "edit", "update", "correct", "actually"]):
        return "edit"
    elif any(word in text for word in ["history", "previous", "past interaction"]):
        return "history"
    elif any(word in text for word in ["summary", "summarize", "brief"]):
        return "summarize"
    elif any(
        phrase in text
        for phrase in [
            "suggest next",
            "suggest action",
            "what next",
            "next best action",
            "what should i do next",
        ]
    ):
        return "suggest"

    # Default to log when user is describing an interaction narrative.
    log_markers = ["met", "discussed", "sentiment", "shared", "doctor", "dr.", "today i"]
    if any(marker in text for marker in log_markers):
        return "log"

    return "log"


# 🔧 Build graph
builder = StateGraph(dict)

# ✅ Add ONLY tool nodes
def route_input(state):
    return state

builder.add_node("route", route_input)
builder.add_node("log", log_interaction)
builder.add_node("edit", edit_interaction)
builder.add_node("suggest", suggest_action)
builder.add_node("history", get_history)
builder.add_node("summarize", summarize)

# ✅ IMPORTANT: entry point must be REAL node
builder.set_entry_point("route")

# ✅ Conditional routing from route node
builder.add_conditional_edges(
    "route",
    router,
    {
        "log": "log",
        "edit": "edit",
        "suggest": "suggest",
        "history": "history",
        "summarize": "summarize",
    }
)

# ✅ End each branch after one tool execution
builder.add_edge("log", END)
builder.add_edge("edit", END)
builder.add_edge("suggest", END)
builder.add_edge("history", END)
builder.add_edge("summarize", END)

graph = builder.compile()