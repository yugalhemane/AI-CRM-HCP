from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import json

from app.database import Base, engine, get_db_session
from app.langgraph_agent import graph
from app.models import InteractionRecord
from app.utils import apply_date_time_defaults, normalize_form_data

app = FastAPI()
Base.metadata.create_all(bind=engine)

# CORS (needed for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend running"}

class ChatRequest(BaseModel):
    message: str | None = None
    input: str | None = None


SESSION_STATE = {
    "form_data": normalize_form_data({}),
    "history": [],
}


def load_recent_history(limit: int = 10):
    with get_db_session() as db:
        rows = (
            db.query(InteractionRecord)
            .order_by(InteractionRecord.created_at.desc())
            .limit(limit)
            .all()
        )
        rows.reverse()
        history = []
        for row in rows:
            try:
                parsed_form = json.loads(row.form_data)
            except Exception:
                parsed_form = {}
            history.append(
                {
                    "user_input": row.user_input,
                    "tool_used": row.tool_used,
                    "assistant_message": row.assistant_message,
                    "form_data": parsed_form,
                    "created_at": row.created_at.isoformat(),
                }
            )
        return history


@app.post("/chat")
async def chat(data: ChatRequest):
    prompt = data.message or data.input
    if not prompt:
        raise HTTPException(
            status_code=400,
            detail="Request body must include either 'message' or 'input'.",
        )

    graph_input = {
        "input": prompt,
        "form_data": SESSION_STATE["form_data"],
        "history": load_recent_history(limit=10),
    }
    result = graph.invoke(graph_input)

    updated_form = apply_date_time_defaults(result.get("form_data", SESSION_STATE["form_data"]))
    SESSION_STATE["form_data"] = updated_form
    SESSION_STATE["history"].append(
        {
            "user_input": prompt,
            "tool_used": result.get("tool_used", "unknown"),
            "form_data": updated_form,
        }
    )

    with get_db_session() as db:
        db.add(
            InteractionRecord(
                user_input=prompt,
                tool_used=result.get("tool_used", "unknown"),
                assistant_message=result.get("assistant_message", "Done."),
                form_data=json.dumps(updated_form),
            )
        )
        db.commit()

    return {
        "tool_used": result.get("tool_used"),
        "assistant_message": result.get("assistant_message", "Done."),
        "form_data": updated_form,
        "suggestion": result.get("suggestion"),
        "summary": result.get("summary"),
        "history": result.get("history"),
        "error": result.get("error"),
    }


@app.post("/reset")
def reset_session():
    SESSION_STATE["form_data"] = normalize_form_data({})
    SESSION_STATE["history"] = []
    with get_db_session() as db:
        db.query(InteractionRecord).delete()
        db.commit()
    return {"message": "Session reset done.", "form_data": SESSION_STATE["form_data"]}


@app.get("/interactions")
def interactions():
    return {"items": load_recent_history(limit=50)}