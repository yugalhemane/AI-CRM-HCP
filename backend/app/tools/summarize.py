from app.utils import llm

def summarize(state):
    text = state.get("input", "")

    prompt = f"Summarize this interaction in 2 concise lines for CRM notes:\n{text}"

    try:
        response = llm.invoke(prompt)
        summary = response.content.strip()
    except Exception as e:
        print("Summarize Error:", e)
        summary = "Could not generate a summary at the moment."

    return {
        "summary": summary,
        "assistant_message": summary,
        "tool_used": "summarize",
    }