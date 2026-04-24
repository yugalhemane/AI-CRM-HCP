from app.utils import apply_date_time_defaults, extract_json_object, llm, normalize_form_data
import re


def apply_explicit_corrections(user_input: str, data: dict) -> dict:
    updated = data.copy()

    name_match = re.search(
        r"(?:name\s+(?:was|is)\s+(?:actually\s+)?)(dr\.?\s+[a-z]+)",
        user_input,
        re.IGNORECASE,
    )
    if name_match:
        updated["hcp_name"] = name_match.group(1).strip()

    if "sentiment was negative" in user_input.lower() or "sentiment is negative" in user_input.lower():
        updated["sentiment"] = "negative"
    elif "sentiment was positive" in user_input.lower() or "sentiment is positive" in user_input.lower():
        updated["sentiment"] = "positive"
    elif "sentiment was neutral" in user_input.lower() or "sentiment is neutral" in user_input.lower():
        updated["sentiment"] = "neutral"

    return updated

def edit_interaction(state):
    current = normalize_form_data(state.get("form_data"))
    user_input = state.get("input", "")

    prompt = f"""
You are updating CRM interaction fields based on user correction.
Only update fields explicitly requested by the user.

Current form data:
{current}

User correction:
{user_input}

Return ONLY JSON with all fields:
{{
  "hcp_name": "",
  "interaction_type": "",
  "date": "",
  "time": "",
  "attendees": "",
  "topics": "",
  "sentiment": "",
  "materials": "",
  "samples_distributed": "",
  "outcomes": "",
  "follow_up_actions": ""
}}
"""

    try:
        response = llm.invoke(prompt)
        parsed = extract_json_object(response.content)
        merged = apply_date_time_defaults({**current, **parsed})
        merged = apply_explicit_corrections(user_input, merged)

        return {
            "form_data": merged,
            "assistant_message": "Updated only the requested fields. Existing values are preserved.",
            "tool_used": "edit_interaction",
        }

    except Exception as e:
        print("Edit Error:", e)
        return {
            "form_data": current,
            "assistant_message": f"I could not apply this edit right now: {str(e)}",
            "tool_used": "edit_interaction",
            "error": "edit_interaction_failed",
        }