# SEO Content Generator

Minimal SEO article generator with a Streamlit frontend and FastAPI backend.

## Overview
- Frontend: [streamlit_app/app.py](streamlit_app/app.py) — UI that posts generation requests to the backend and displays results.
- Backend: [backend/app/main.py](backend/app/main.py) — FastAPI exposing job endpoints. Generation flow implemented in [`app.services.job_runner.run_full_generation`](backend/app/services/job_runner.py).
- SERP fetcher: [`app.services.serp_provider.MockSerpProvider`](backend/app/services/serp_provider.py) — fetches top 10 results and prints JSON logs.
- Content generator: [`app.agents.content_agent.ContentAgent`](backend/app/agents/content_agent.py) — calls OpenAI to produce structured article JSON.
- Job model/store: [`app.models.job.GenerationJob.create`](backend/app/models/job.py) and [backend/app/services/job_store.py](backend/app/services/job_store.py).

## Prerequisites
- Python 3.10+ recommended
- OpenAI API key and SERP API key for production (set in backend/.env or environment)

## Setup (recommended: create separate venvs for frontend/backend)

Backend:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate    # mac/linux
# .venv\Scripts\activate      # windows
pip install -r [requirements.txt]
# create/edit .env with your OPENAI_API_KEY and SERP_API_KEY (see backend/.env.example)

Frontend:
cd streamlit_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r [requirements.txt]


Run
Start backend (from the backend folder):
uvicorn app.main:app --reload


Frontend will call backend endpoints:

POST /jobs -> create a GenerationJob
POST /jobs/{id}/run -> trigger generation (runs run_full_generation)
GET /jobs/{id}/result -> fetch result JSON
Environment (.env)
Place keys in backend/.env or export environment variables:

OPENAI_API_KEY
SERP_API_KEY (or Serp_API_key)
Do NOT commit .env (it's in .gitignore).
