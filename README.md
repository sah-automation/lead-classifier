# Lead Classifier — Automated Lead Management System

A small end-to-end lead automation system with three parts: a Python FastAPI backend, an n8n automation workflow, and a Next.js frontend dashboard. Inbound leads are automatically classified as Hot, Warm, or Cold using Google Gemini and displayed in a clean, filterable dashboard.

---

## Architecture

```
┌─────────────────────┐       ┌──────────────────────────┐       ┌──────────────────────┐
│   Google Sheet      │──────▶│   n8n Workflow           │──────▶│  Slack Notification  │
│  (Lead Source)      │       │  (Trigger + HTTP Request)│       │  (Team Alert)        │
└─────────────────────┘       └────────────┬─────────────┘       └──────────────────────┘
                                            │
                                    POST /lead
                                            │
                                            ▼
                               ┌────────────────────────┐
                               │   FastAPI Backend      │
                               │   ─────────────────    │
                               │   routes/leads.py      │
                               │   routes/classify.py   │
                               │   services/            │
                               │     gemini_service.py  │
                               │     lead_service.py    │
                               │   database.py (SQLite) │
                               └────────────┬───────────┘
                                            │
                                      GET /leads
                                   PATCH /lead/{id}/contacted
                                            │
                                            ▼
                               ┌────────────────────────┐
                               │   Next.js Dashboard    │
                               │   ─────────────────    │
                               │   Filter by class.     │
                               │   Color-coded badges   │
                               │   Mark as Contacted    │
                               └────────────────────────┘
```

---

## How to Run Locally

### Part 1 — Python Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Add your Gemini API key to `.env`:

```
GEMINI_API_KEY=your_key_here
```

Start the server:

```bash
uvicorn main:app --reload --port 8000
```

API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Part 2 — n8n Automation Workflow

1. Install n8n locally (free, open source):
   ```bash
   npx n8n
   ```
2. Open [http://localhost:5678](http://localhost:5678)
3. Import the workflow: **Menu → Import from File → `automation/lead-classifier-workflow.json`**
4. Configure credentials:
   - Google Sheets OAuth2
   - Slack Incoming Webhook URL
   - Update the HTTP Request node URL to your backend (use ngrok if running locally: `ngrok http 8000`)
5. Activate the workflow

---

### Part 3 — Next.js Frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard available at: [http://localhost:3000](http://localhost:3000)

Make sure the backend is running on port 8000 before opening the dashboard.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/lead` | Accept a new lead, classify via Gemini, store in SQLite |
| `GET` | `/leads` | Return all leads with classification and suggested reply |
| `POST` | `/classify` | Standalone classify — takes `{message}`, returns `{classification, suggested_reply}` |
| `PATCH` | `/lead/{id}/contacted` | Mark a lead as contacted |

---

## Project Structure

```
lead-classifier/
│
├── backend/
│   ├── main.py                  # FastAPI app, router registration, lifespan
│   ├── config.py                # Env var loader (GEMINI_API_KEY, DATABASE_URL)
│   ├── database.py              # SQLite connection, init_db(), context manager
│   ├── models/
│   │   └── lead.py              # Pydantic models: LeadCreate, LeadResponse, etc.
│   ├── routes/
│   │   ├── leads.py             # POST /lead, GET /leads, PATCH /lead/{id}/contacted
│   │   └── classify.py          # POST /classify
│   ├── services/
│   │   ├── lead_service.py      # DB logic: insert, fetch, update
│   │   └── gemini_service.py    # Gemini API call, retry logic, fallback
│   ├── .env                     # GEMINI_API_KEY (not committed)
│   └── requirements.txt
│
├── automation/
│   └── lead-classifier-workflow.json   # n8n workflow export
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx             # Homepage — fetches leads, renders dashboard
│   ├── components/
│   │   ├── leads-table.tsx      # Main table with all required columns
│   │   ├── filter-bar.tsx       # Hot/Warm/Cold filter dropdown
│   │   └── status-badge.tsx     # Color-coded classification badge
│   ├── lib/
│   │   └── api.ts               # API helper functions (getLeads, markAsContacted)
│   └── types/
│       └── lead.ts              # TypeScript Lead type and LeadClassification
│
└── README.md
```

---

## Libraries, APIs & Tools Used

| Tool / Library | Why |
|---|---|
| **FastAPI** | Modern typed Python API framework with automatic validation via Pydantic and built-in Swagger docs |
| **Pydantic v2** | Input/output validation and serialization — enforces typed contracts between frontend and backend |
| **SQLite + sqlite3** | Zero-setup file-based database, built into Python — sufficient for local demo as brief allowed |
| **Google Gemini (`gemini-2.5-flash`)** | Fast, cost-effective LLM with a generous free tier — classification + reply generation in one call |
| **google-generativeai** | Official Python SDK for Gemini API |
| **python-dotenv** | Loads `.env` file for secrets — keeps API keys out of source code |
| **n8n** | Free, open-source automation tool — runs locally, exports as JSON, visual workflow editor |
| **Next.js 15 (App Router)** | React framework preferred by the team — App Router gives clean file-based routing |
| **Tailwind CSS v4** | Utility-first CSS — fast to write, consistent design, minimal custom CSS needed |
| **TypeScript** | Type safety across the frontend — catches bugs at compile time, improves IDE support |

---

## Tradeoffs Made

**SQLite over PostgreSQL** — The brief explicitly allowed SQLite and deployment to production was out of scope. SQLite requires zero setup and the single `.db` file is easy to inspect and share. In production, a migration to PostgreSQL with proper indexing would be the right move.

**Synchronous Gemini calls** — The Gemini SDK call is synchronous (blocking), which is fine for a single-user local demo. In production with concurrent requests, async calls using `asyncio` and `httpx` would be required so the server doesn't stall while waiting for the LLM.

**Text parsing over JSON mode** — Instead of asking Gemini for strict JSON output (which can be brittle — Gemini sometimes wraps it in markdown fences), the prompt asks for a clean two-line response and Python parses it. More robust for a demo; native JSON mode would be better at scale.

**Inline prompt in service file** — The Gemini prompt lives inside `gemini_service.py` for simplicity. With more time, it would move to a config file or prompt registry so it can be tuned without touching service logic.

**CORS set to allow all origins** — Acceptable for local development. In production, `allow_origins` would be restricted to the actual frontend domain only.

---

## Further Improvements if Required

1. **Async LLM calls** — Use `asyncio` and the async Gemini client so concurrent lead submissions don't block each other
2. **Structured output** — Use Gemini's native JSON response mode for more reliable parsing instead of text-line parsing
3. **Background classification queue** — Store the lead immediately and classify asynchronously via Celery + Redis, so the API responds in under 100ms regardless of Gemini latency
4. **`llm_status` field in DB** — Track whether classification came from a live LLM call or a fallback, so the team can filter and manually review fallback leads
5. **Deduplication** — Check for existing leads by email + source before inserting to prevent duplicates on workflow re-runs
6. **Environment-specific CORS** — Restrict allowed origins per environment (dev vs. production)
7. **n8n error branch** — Add an error handler node that sends a Slack alert if the backend HTTP request fails, so no lead silently drops

---

## Sample Test Data

The `sample_leads.csv` file contains 10 fake leads provided as standard test input. To load them into the backend:

```bash
cd backend
python scripts/seed_leads.py
```

Or submit them one by one via the Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).
