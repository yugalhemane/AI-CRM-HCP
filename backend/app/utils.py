import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

DEFAULT_FORM_DATA = {
    "hcp_name": "",
    "interaction_type": "Meeting",
    "date": "",
    "time": "",
    "attendees": "",
    "topics": "",
    "sentiment": "",
    "materials": "",
    "samples_distributed": "",
    "outcomes": "",
    "follow_up_actions": "",
}


def extract_json_object(raw_text: str) -> dict:
    if not raw_text:
        return {}

    try:
        parsed = json.loads(raw_text)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", raw_text)
    if not match:
        return {}

    try:
        parsed = json.loads(match.group(0))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def normalize_form_data(raw_form_data: dict | None) -> dict:
    safe = DEFAULT_FORM_DATA.copy()
    if isinstance(raw_form_data, dict):
        for key in safe:
            value = raw_form_data.get(key, "")
            safe[key] = value if isinstance(value, str) else str(value)
    return safe


def apply_date_time_defaults(form_data: dict) -> dict:
    """Ensure date/time are always populated for UI completeness."""
    updated = normalize_form_data(form_data)

    date_raw = (updated.get("date") or "").strip().lower()
    if date_raw in ("", "today", "now"):
        updated["date"] = datetime.now().strftime("%Y-%m-%d")

    time_raw = (updated.get("time") or "").strip()
    if time_raw == "":
        updated["time"] = datetime.now().strftime("%I:%M %p").lstrip("0")

    # Normalize sentiment to expected tokens
    sent = (updated.get("sentiment") or "").strip().lower()
    if sent in ("positive", "neutral", "negative"):
        updated["sentiment"] = sent

    return updated


llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    # Prevent one user request from triggering multiple Groq retries on 429.
    max_retries=0,
    timeout=30,
)