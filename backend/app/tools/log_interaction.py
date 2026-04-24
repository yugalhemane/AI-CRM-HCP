from app.utils import apply_date_time_defaults, extract_json_object, llm, normalize_form_data

def log_interaction(state):
    user_input = state.get("input", "")
    current_form = normalize_form_data(state.get("form_data"))

    prompt = f"""
You are an AI CRM assistant for healthcare field reps.
Extract structured interaction data from the user's message.

Current form values:
{current_form}

User message:
{user_input}

Return ONLY JSON:
{{
  "hcp_name": "",
  "interaction_type": "Meeting|Call|Email|Conference|Other",
  "date": "YYYY-MM-DD or 'today'",
  "time": "",
  "attendees": "",
  "topics": "",
  "sentiment": "positive|neutral|negative",
  "materials": "",
  "samples_distributed": "",
  "outcomes": "",
  "follow_up_actions": ""
}}
"""

    try:
        response = llm.invoke(prompt)
        parsed = extract_json_object(response.content)
        merged = apply_date_time_defaults({**current_form, **parsed})

        return {
            "form_data": merged,
            "assistant_message": "Interaction logged successfully. I extracted and filled the form from your message.",
            "tool_used": "log_interaction",
        }

    except Exception as e:
        print("Log Interaction Error:", e)
        return {
            "form_data": current_form,
            "assistant_message": f"I could not extract the interaction details right now: {str(e)}",
            "tool_used": "log_interaction",
            "error": "log_interaction_failed",
        }