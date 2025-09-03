# LIMS Deviation Backend (FastAPI + PostgreSQL)

## Setup
1) Create PostgreSQL DB (e.g. `lims`), then run the SQL:
```bash
psql -U postgres -d lims -f backend/schema.sql
```
2) Copy env:
```bash
cp backend/.env.example backend/.env
```
3) Install deps & start:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Key Endpoints
- POST /deviations
- GET /deviations
- PATCH /deviations/{id}/review
- PATCH /deviations/{id}/accept
- PATCH /deviations/{id}/reject
- PATCH /deviations/{id}/resolve
- PATCH /deviations/{id}/close
- GET /data/customers, /data/srfs, /data/equipments/{srf_id}
