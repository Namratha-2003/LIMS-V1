# LIMS Deviation Module (Full Stack)

This bundle includes:
- `backend/` FastAPI + PostgreSQL
- `frontend/` React (Vite)
- `backend/schema.sql` for the 7 required tables

## Quickstart

### 1) Database
Create a PostgreSQL database (e.g. `lims`) and run:
```bash
psql -U postgres -d lims -f backend/schema.sql
```

### 2) Backend
```bash
cp backend/.env.example backend/.env
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3) Seed minimal demo data (optional)
In `psql`:
```sql
INSERT INTO customers(name,email,phone) VALUES ('ACME Labs','acme@example.com','9999999999');
INSERT INTO srfs(customer_id,srf_number) VALUES (1,'SRF-0001');
INSERT INTO srf_equipments(srf_id,equipment_name,equipment_serial) VALUES (1,'Weighing Scale','WS-123');
```

### 4) Frontend
```bash
cd frontend
npm i
npm run dev
```
Open `http://localhost:5173`

### Flow
1. Technician logs a deviation in `/technician`.
2. QA marks it **IN_REVIEW** in `/qa`.
3. Customer goes to `/customer` to **Accept** or **Reject**.
4. QA can **Resolve** then **Close** in `/qa`.

Notifications are stored in DB and email is logged to `/mnt/data/email_log.txt` unless SMTP is configured.

---

> This is a minimal, clean scaffold you can extend with auth, RBAC, richer timelines, and real SMS/email gateways.
