from app.utils import llm

def suggest_action(state):
    data = state.get("form_data", "")
    user_input = state.get("input", "")

    prompt = f"""
Based on this interaction:
{data}

User request:
{user_input}

Suggest 1 practical next best action for the sales rep in 1-2 lines.
"""

    try:
        response = llm.invoke(prompt)
        suggestion = response.content.strip()
        return {
            "suggestion": suggestion,
            "assistant_message": suggestion,
            "tool_used": "suggest_action",
        }
    except Exception as e:
        print("Suggest Error:", e)
        fallback = "Suggested next action: schedule a follow-up call and share evidence summary with the HCP."
        return {
            "suggestion": fallback,
            "assistant_message": f"{fallback} (fallback used due to temporary LLM issue)",
            "tool_used": "suggest_action",
            "error": "suggest_action_failed",
        }