# Course Catalog Service

FastAPI microservice responsible for creating, listing, retrieving, updating and deleting course records.

## Local run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
uvicorn app.main:app --reload --port 8001
```
Open http://localhost:8001/docs. Set `DATABASE_URL=sqlite:///./data/catalog.db` if desired.
