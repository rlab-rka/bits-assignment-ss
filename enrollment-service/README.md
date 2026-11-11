# Enrollment Management Service

FastAPI microservice responsible for student course registrations. It validates course IDs by calling the Course Catalog Service over HTTP.

## Local run
Start Course Catalog on port 8001 first. Then:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
COURSE_CATALOG_URL=http://localhost:8001 uvicorn app.main:app --reload --port 8002
```
Open http://localhost:8002/docs.
