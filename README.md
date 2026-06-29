# 👟 SunnyStep Retail Revenue Optimizer

AI-powered retail insights and revenue recommendations for SunnyStep Singapore — a comfort footwear brand with 12 stores island-wide.

**Live Demo**: https://sunnystep-retail-revenue-ai.onrender.com

---

## What It Does

Retail staff and managers input store KPIs (revenue, transactions, conversion rate, stockouts, customer feedback) and receive instant AI-generated analysis including:

- Store health rating (Excellent / Good / Average / Poor)
- Key findings and root cause analysis
- Prioritised action recommendations with expected impact
- Revenue opportunity identification
- Executive summary

---

## System Design

```
┌─────────────────────────────────────────────────────────┐
│                    User (Browser)                        │
│              Streamlit Frontend (app.py)                 │
│   Input: Store KPIs, Inventory, Customer Feedback        │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP POST /analyze
                      │ JSON payload
                      ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)                   │
│                                                          │
│  1. Receives retail data payload                         │
│  2. Constructs structured prompt (prompts.py)            │
│  3. Calls OpenAI GPT-4o-mini                            │
│  4. Parses JSON response                                 │
│  5. Returns structured insights                          │
└─────────────────────┬───────────────────────────────────┘
                      │ API call
                      ▼
┌─────────────────────────────────────────────────────────┐
│              OpenAI GPT-4o-mini                          │
│   Input:  Retail context + KPI data                      │
│   Output: store_health, key_findings, root_causes,       │
│           recommended_actions, revenue_opportunities,    │
│           summary                                        │
└─────────────────────────────────────────────────────────┘
```

### Architecture

| Layer | Technology | Role |
|---|---|---|
| Frontend | Streamlit | Dashboard UI, KPI inputs, results display |
| Backend | FastAPI + Uvicorn | REST API, prompt engineering, response parsing |
| AI Model | OpenAI GPT-4o-mini | Retail analysis and recommendation generation |
| Deployment | Render (2 services) | Cloud hosting with env var config |
| Version Control | GitLab | CI/CD ready repository |

### Prompt Engineering

The system uses a structured input/output prompt pattern:

**Input prompt** — retail context injected into the user message:
```
Store: {store_name} | Month: {month}
Revenue: {revenue} | Transactions: {transactions}
AOV: {aov} | Conversion: {conversion_rate}%
Stockouts: {stockouts} | Slow movers: {slow_moving}
Best sellers: {best_sellers}
Customer feedback: {feedback}
```

**Output schema** — model returns strict JSON:
```json
{
  "store_health": "Excellent | Good | Average | Poor",
  "key_findings": ["...", "..."],
  "root_causes": ["...", "..."],
  "recommended_actions": [
    {
      "priority": "High | Medium | Low",
      "action": "...",
      "expected_impact": "..."
    }
  ],
  "revenue_opportunities": ["...", "..."],
  "summary": "..."
}
```

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

Run locally:
```bash
uvicorn main:app --reload          # Terminal 1 — FastAPI on :8000
streamlit run app.py               # Terminal 2 — Streamlit on :8501
```

Open: http://localhost:8501

---

## Deployment (Render)

Two separate web services on Render:

**Service 1 — FastAPI backend**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Env: `OPENAI_API_KEY`

**Service 2 — Streamlit frontend**
- Build: `pip install -r requirements.txt`
- Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Env: `API_URL` = URL of Service 1

---

## Built For

This prototype was built specifically for SunnyStep as part of an AI Engineer interview — demonstrating end-to-end AI product thinking, prompt engineering, and full-stack deployment.

**Stack**: Python · FastAPI · Streamlit · OpenAI API · Render · GitLab
