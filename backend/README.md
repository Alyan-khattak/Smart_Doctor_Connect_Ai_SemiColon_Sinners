# Smart Doctor Connect AI — Backend

FastAPI backend for the Smart Doctor Connect AI hackathon project.

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Run

```bash
# Copy demo env
cp ../demo.env .env

# Seed database
python -m app.seed

# Start server
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```

## API Docs

Visit: http://localhost:8000/docs

## Endpoints

- GET /health
- GET /doctors
- GET /doctors/{id}
- POST /doctors
- PUT /doctors/{id}
- GET /doctors/search
- POST /recommendations
- GET /availability/{doctor_id}?date=YYYY-MM-DD
- POST /availability/{doctor_id}
- PUT /availability/slot/{slot_id}
- POST /appointments
- GET /appointments/doctor/{doctor_id}
- GET /appointments/{appointment_id}
- PUT /appointments/{appointment_id}/status
- POST /chatbot/message
- POST /chatbot/lead
- GET /chatbot/leads/{doctor_id}
- POST /email/send-appointment
- POST /email/send-lead
- GET /dashboard/doctor/{doctor_id}
