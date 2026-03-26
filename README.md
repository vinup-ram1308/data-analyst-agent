# CSV Analyst Agent

A production-ready AI agent built with Google Agent Development Kit (ADK)
and Gemini, deployed on Google Cloud Run.

## What it does

Accepts a CSV dataset as input and returns a structured Markdown analysis report containing:

- **Dataset Overview** — row count, column count, duplicate detection
- **Data Quality Check** — missing values per column with percentages and status
- **Statistical Summary** — mean, median, std dev, min, max, percentiles for all numeric columns
- **Categorical Summary** — unique value counts and top value distribution

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Agent  | Google Agent Development Kit (ADK) |
| Model     | Gemini 2.0 Flash (Vertex AI) |
| Deployment | Google Cloud Run (serverless) |
| Auth | IAM service account |
| Language | Python 3.12 |

## Architecture
```
User (HTTP)
    │
    ▼
Cloud Run — ADK Agent Service
    │
    └── root_agent (Gemini 2.0 Flash)
            │
            └── analyze_csv() tool
                    ├── Data quality check   (pandas)
                    ├── Statistical summary  (pandas)
                    └── Markdown report generation
```

## Project Structure
```
data_analyst_agent/
├── __init__.py       # ADK package entry point
├── agent.py          # Root agent definition
├── tools.py          # analyze_csv tool (all analysis logic)
└── requirements.txt  # Dependencies
```

## How to run locally
```bash
# 1. Clone the repo
git clone https://github.com/vinup-ram1308/data-analyst-agent.git
cd data-analyst-agent

# 2. Create virtual environment
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt

# 3. Set up .env
cp .env.example .env
# Fill in your PROJECT_ID and credentials

# 4. Run locally
cd ~
adk web
```

## How to deploy
```bash
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=data-analyst-agent \
  --with_ui \
  . \
  -- \
  --service-account=$SERVICE_ACCOUNT
```

## Sample input
```
name,age,salary,department
Alice,30,75000,Engineering
Bob,25,60000,Marketing
Charlie,35,,Engineering
Alice,30,75000,Engineering
Diana,28,80000,
```

## Live demo

Cloud Run URL: `https://data-analyst-agent-xxxx.run.app`

---

*Built for Google Cloud Gen AI Academy APAC 2026 — Cohort 1, Track 1*
