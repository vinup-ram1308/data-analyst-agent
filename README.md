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
employee_id,name,age,gender,department,job_title,years_at_company,salary,performance_score,training_hours,last_promotion_year,is_remote,city
E001,Alice Johnson,34,Female,Engineering,Senior Engineer,6,95000,4.5,40,2022,True,Bangalore
E002,Bob Smith,28,Male,Marketing,Marketing Analyst,3,62000,3.8,20,2021,False,Mumbai
E003,Carol White,45,Female,Engineering,Engineering Manager,12,130000,4.9,15,2023,False,Delhi
E004,David Brown,31,Male,Sales,Sales Executive,5,58000,3.2,25,2020,False,Chennai
E005,Eve Davis,27,Female,HR,HR Coordinator,2,48000,4.1,30,,True,Bangalore
E006,Frank Miller,52,Male,Finance,Finance Director,20,145000,4.7,10,2019,False,Mumbai
E007,Grace Wilson,29,Female,Engineering,Junior Engineer,1,72000,3.9,50,2023,True,Hyderabad
E008,Henry Moore,38,Male,Marketing,Marketing Manager,9,88000,4.3,18,2021,False,Delhi
E009,Irene Taylor,33,Female,Sales,Senior Sales Executive,7,74000,4.6,22,2022,True,Bangalore
E010,James Anderson,41,Male,Engineering,Senior Engineer,10,102000,4.2,35,2020,False,Pune
E011,Karen Thomas,26,Female,HR,HR Assistant,1,42000,3.5,28,,False,Mumbai
E012,Liam Jackson,36,Male,Finance,Financial Analyst,8,79000,4.0,12,2021,True,Bangalore
E013,Mia Harris,30,Female,Engineering,Engineer,4,83000,4.4,45,2022,True,Hyderabad
E014,Noah Martin,44,Male,Sales,Sales Manager,11,96000,4.1,20,2019,False,Chennai
E015,Olivia Garcia,25,Female,Marketing,Junior Marketer,1,51000,3.7,35,2023,True,Delhi
E016,Paul Martinez,39,Male,Engineering,Engineering Lead,8,118000,4.8,30,2022,False,Bangalore
E017,Quinn Robinson,32,Female,Finance,Senior Analyst,6,86000,4.3,14,2021,True,Mumbai
E018,Ryan Lee,47,Male,HR,HR Manager,15,91000,4.5,22,2020,False,Pune
E019,Sara Walker,28,Female,Sales,Sales Executive,3,56000,3.4,18,,False,Hyderabad
E020,Tom Hall,35,Male,Engineering,Engineer,5,88000,4.1,40,2022,True,Bangalore
E021,Uma Allen,43,Female,Marketing,Marketing Director,14,125000,4.6,12,2019,False,Delhi
E022,Victor Young,29,Male,Engineering,Junior Engineer,2,69000,3.6,55,2023,True,Pune
E023,Wendy King,37,Female,Finance,Finance Manager,9,99000,4.4,16,2021,False,Mumbai
E024,Xander Wright,31,Male,Sales,Sales Executive,4,61000,3.9,20,2022,False,Chennai
E025,Yara Scott,26,Female,HR,HR Coordinator,2,46000,3.8,32,,True,Bangalore
E026,Zack Green,50,Male,Engineering,Principal Engineer,18,138000,4.9,25,2018,False,Delhi
E027,Amy Baker,34,Female,Marketing,Marketing Analyst,5,67000,4.0,22,2021,True,Hyderabad
E028,Brian Adams,40,Male,Finance,Financial Analyst,10,84000,4.2,10,2020,False,Pune
E029,Chloe Nelson,27,Female,Engineering,Junior Engineer,2,71000,3.7,48,2023,True,Bangalore
E030,Daniel Carter,55,Male,Sales,VP of Sales,22,,4.8,8,2017,False,Mumbai
E031,Ella Mitchell,33,Female,HR,HR Specialist,6,63000,4.3,26,2021,False,Delhi
E032,Felix Perez,29,Male,Engineering,Engineer,3,80000,4.0,42,2022,True,Hyderabad
E033,Gina Roberts,38,Female,Finance,Senior Analyst,8,89000,4.5,14,2021,False,Bangalore
E034,Harry Turner,45,Male,Marketing,Marketing Manager,12,93000,4.1,16,2020,False,Chennai
E035,Isla Phillips,30,Female,Engineering,Engineer,4,84000,4.3,38,2022,True,Pune
E036,Jack Campbell,36,Male,Sales,Senior Sales Executive,8,78000,4.4,20,2021,False,Mumbai
E037,Katie Parker,28,Female,HR,HR Assistant,1,43000,3.6,30,,False,Delhi
E038,Leo Evans,42,Male,Engineering,Senior Engineer,10,106000,4.6,32,2020,False,Bangalore
E039,Maya Edwards,31,Female,Finance,Financial Analyst,5,77000,4.1,12,2022,True,Hyderabad
E040,Nathan Collins,27,Male,Marketing,Junior Marketer,1,52000,3.8,38,2023,True,Pune
E001,Alice Johnson,34,Female,Engineering,Senior Engineer,6,95000,4.5,40,2022,True,Bangalore
E008,Henry Moore,38,Male,Marketing,Marketing Manager,9,88000,4.3,18,2021,False,Delhi
```

## Live demo

Cloud Run URL: `https://data-analyst-agent-yhmlqfpbzq-uc.a.run.app`

---

*Built for Google Cloud Gen AI Academy APAC 2026 — Cohort 1, Track 1*
