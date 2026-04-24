# AI‑First CRM (HCP Module) — Log Interaction Screen

This repo implements the **Task 1** “Log Interaction Screen” with:

- **Frontend**: React + Redux + Bootstrap grid (responsive split layout)
- **Backend**: FastAPI (Python)
- **Agent Framework**: LangGraph
- **LLM**: Groq (model set via env)
- **Database**: Postgres / MySQL (SQLAlchemy)
- **Font**: Inter (Google Fonts)

> Rule enforced: **Do not manually edit the left form** — it is read‑only and only updated via the AI Assistant chat.

---

## Project structure

- `frontend/` — React app (Vite)
- `backend/` — FastAPI app

---

## Backend setup (FastAPI + LangGraph)

### 1) Create environment file

Copy:

- `backend/.env.example` → `backend/.env`

Fill:

- `GROQ_API_KEY`
- `GROQ_MODEL`
- `DATABASE_URL` (**must be Postgres or MySQL for final submission**)

### 2) Database (recommended Postgres via Docker)

From repo root:

```bash
docker compose up -d
```

Then in `backend/.env`:

```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/hcp_crm
```

### 3) Install backend dependencies

```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### 4) Run backend

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend will be at `http://127.0.0.1:8000`.

---

## Frontend setup (React + Redux + Bootstrap)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be at the Vite URL shown in terminal.

---

## LangGraph tools (5 tools)

The LangGraph agent routes each user chat prompt to one of the tools below.

1. **Log Interaction (`log_interaction`)**
   - Extracts structured interaction fields from natural language
   - Updates the form automatically
2. **Edit Interaction (`edit_interaction`)**
   - Applies user corrections to the existing form without manual edits
3. **Suggest Next Action (`suggest_action`)**
   - Produces a recommended follow‑up action for the rep
4. **Summarize (`summarize`)**
   - Creates concise notes for CRM
5. **Get History (`get_history`)**
   - Summarizes recent interactions from stored history

---

## Demo script (prompts to show all 5 tools)

Use these in the **AI Assistant chat** in this order (recommended for video).

### A) Reset (optional)
- Click the **Reset** button in the chat panel.

### B) Log Interaction (Tool: `log_interaction`)
Paste:

> Today I met with Dr. Smith and discussed Product X efficiency. The sentiment was positive and I shared brochures. I distributed 5 starter samples. Outcome: doctor agreed to evaluate in next cycle. Follow-up: schedule a revisit next week.

Expected:
- Left form fills HCP name, date/time, sentiment, materials, samples, outcomes, follow‑up.

### C) Edit Interaction (Tool: `edit_interaction`)
Paste:

> Sorry, the name was actually Dr. John and the sentiment was negative.

Expected:
- Only name + sentiment change, other fields stay unchanged.

### D) Summarize (Tool: `summarize`)
Paste:

> Summarize this interaction for CRM notes.

### E) Suggest Next Action (Tool: `suggest_action`)
Paste:

> Suggest next best action for this HCP.

### F) History (Tool: `get_history`)
Paste:

> Show history of recent interactions.

---

## API endpoints

- `POST /chat` — main chat endpoint (routes to tools via LangGraph)
- `POST /reset` — clears session + stored interaction rows
- `GET /interactions` — returns stored interaction records

---

## Notes about Groq model requirement

The assignment document mentions `gemma2-9b-it`. Groq can deprecate models over time.

For evaluation:
- Use a **currently supported Groq model**
- Set it in `GROQ_MODEL`
- Mention in your video/README what model you used and why (if `gemma2-9b-it` is not available on Groq at the time).

---

## Video checklist (10–15 minutes)

- Show the split screen UI (responsive behavior)
- Demonstrate **all 5 tools** using the prompts above
- Explain flow:
  - Frontend → `/chat` → LangGraph router → tool → response → Redux updates form
- Show DB persistence quickly:
  - open `GET /interactions` in `/docs` and show records are stored

