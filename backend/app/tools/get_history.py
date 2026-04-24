from app.utils import llm

def get_history(state):
    history = state.get("history", [])
    recent_history = history[-5:] if isinstance(history, list) else []

    prompt = f"""
You are an AI CRM assistant.
Summarize this recent interaction history in 2 short bullet points.
If history is empty, say no prior interactions found.

History:
{recent_history}
"""

    try:
        response = llm.invoke(prompt)
        history_text = response.content.strip()
    except Exception as e:
        print("History Error:", e)
        history_text = "No prior interactions found in this session."

    return {
        "history": history_text,
        "assistant_message": history_text,
        "tool_used": "get_history",
    }