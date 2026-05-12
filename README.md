# Smart Doctor Connect AI

Smart Doctor Connect AI is a healthcare web application built for the MTM AI Hackathon by GDGoC CUI Wah. It helps patients in Pakistan search for doctors by symptoms, city, specialization, and consultation type, then book appointments or use an AI assistant when a doctor is unavailable.

The project currently uses a FastAPI backend, SQLite database, Next.js frontend, Groq for AI routing/chat assistance, and SMTP email delivery.

---

## Current Feature Set

- Patient search by symptoms, city, specialization, and consultation type
- AI symptom-to-specialization routing using Groq with keyword fallback
- Doctor recommendation ranking by specialization, city, availability, consultation type, rating, and experience
- Public doctor profile pages
- Doctor registration/login with JWT
- Doctor profile creation and update flow
- Correct post-login redirect:
  - completed doctor profile -> `/dashboard/doctor`
  - incomplete doctor profile -> `/doctor/profile/edit`
- Role-aware navbar:
  - patients see search and doctor auth links
  - logged-in doctors see dashboard, profile, and logout only
- Conflict-free appointment booking
- Automatic default availability slots for newly created doctor profiles
- Patient email is required during appointment booking
- Appointment email notification to both doctor and patient through SMTP
- Patient-side AI chatbot for unavailable doctor lead capture
- Chatbot collects patient name, email, and problem
- Doctor dashboard showing appointments, chatbot leads, stats, and doctor-side assistant
- Docker-ready backend/frontend setup

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Groq SDK
- SMTP email through Python `smtplib`
- JWT auth with `python-jose`
- Password hashing with `passlib`
- Pytest

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- Lucide React icons

### Runtime Services

- Database: SQLite
- AI: Groq
- Email: SMTP with STARTTLS on port `587`

No Supabase client, Supabase Auth, Supabase Realtime, Firebase, or frontend database client is used.

---

## Project Structure

```txt
.
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── seed.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json
│   └── Dockerfile
├── .env.example
├── demo.env
├── docker-compose.yml
├── context.md
├── idea.md
├── planning.md
├── schema.md
├── backend_agent.md
├── frontend_agent.md
└── AGENTS.md
```

---

## Environment Variables

Create backend and deployment environment values from `.env.example`.

```env
DATABASE_URL=sqlite:///./smart_doctor.db
GROQ_API_KEY=replace_with_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=replace_with_username
SMTP_PASSWORD=xxxxxxxxxxxxxxx
SMTP_FROM_EMAIL=sender_email
SMTP_FROM_NAME="Smart Doctor Connect AI"

APP_PUBLIC_URL=http://localhost:8501
ENABLE_EMAIL=true
ENABLE_GROQ=true

FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

NEXT_PUBLIC_API_URL=http://localhost:8000

JWT_SECRET_KEY=replace_with_secure_secret_for_jwt_auth
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

For Gmail SMTP, use an app password, not the normal account password. Email sending is skipped safely when `ENABLE_EMAIL=false`.

---

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

Backend URLs:

```txt
API: http://localhost:8000
Swagger: http://localhost:8000/docs
Health: http://localhost:8000/health
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```txt
http://localhost:3000
```

---

## Docker

From the project root:

```bash
docker compose --env-file demo.env up --build
```

Validate Compose config:

```bash
docker compose --env-file demo.env config
```

---

## Tests

Backend:

```bash
cd backend
$env:ENABLE_EMAIL='false'; pytest -q
```

Frontend:

```bash
cd frontend
npm run build
```

Current verification status:

```txt
Backend tests: 32 passed
Frontend build: passed
Docker Compose config: passed
```

---

## Main User Flows

### Patient Search and Booking

1. Open `/`.
2. Search symptoms, city, and consultation type.
3. Open a doctor profile.
4. Select an appointment slot.
5. Enter patient name, patient email, medical problem, date, time, and consultation type.
6. Submit booking.
7. Backend saves appointment, marks the slot booked, and attempts email to both doctor and patient.

### Duplicate Booking Protection

The backend prevents two appointments for the same:

```txt
doctor_id + appointment_date + appointment_time
```

If a slot is already booked, the API returns alternative available slots.

### Patient-Side Chatbot

1. Open `/chat/{doctorId}`.
2. Chatbot collects:
   - patient full name
   - patient email
   - problem
3. Backend saves the lead.
4. Backend attempts doctor email notification.

### Doctor Account Flow

1. Register at `/doctor/register`.
2. Complete profile at `/doctor/profile/edit`.
3. After save, redirect goes to `/dashboard/doctor`.
4. Future logins go directly to `/dashboard/doctor` if the profile exists.
5. Logged-in doctor navbar shows Dashboard, Profile, and Logout only.

### Doctor Dashboard

The dashboard shows:

- doctor information
- appointment stats
- appointment table
- chatbot lead table
- doctor-side assistant for dashboard summaries

---

## API Summary

Core public/demo endpoints:

```txt
GET    /health
GET    /doctors
GET    /doctors/{doctor_id}
GET    /doctors/search
POST   /recommendations
GET    /availability/{doctor_id}
POST   /appointments
GET    /appointments/doctor/{doctor_id}
PUT    /appointments/{appointment_id}/status
POST   /chatbot/message
POST   /chatbot/lead
GET    /chatbot/leads/{doctor_id}
GET    /dashboard/doctor/{doctor_id}
```

Doctor auth/profile endpoints:

```txt
POST   /auth/doctor/register
POST   /auth/doctor/login
GET    /auth/doctor/me
GET    /doctors/me/profile
POST   /doctors/me/profile
PUT    /doctors/me/profile
GET    /dashboard/me
```

Email test endpoints:

```txt
POST   /email/send-appointment
POST   /email/send-lead
```

---

## Database Notes

The app uses SQLite through SQLAlchemy. Existing core tables:

- `doctors_auth`
- `doctors`
- `availability_slots`
- `appointments`
- `chatbot_leads`

No schema changes are required for patient email. The existing `patient_contact` field is used by the UI as the patient email field so API contracts remain stable.

---

## Email Behavior

SMTP is used instead of Resend.

Rules:

- SMTP uses STARTTLS on port `587`.
- Config is read only from environment variables.
- If `ENABLE_EMAIL=false`, email sending is skipped and logged.
- If SMTP fails, the appointment or lead still stays saved.
- Booking attempts email to both:
  - doctor email from doctor profile
  - patient email from booking form
- Chatbot lead attempts email to the doctor.

---

## Troubleshooting

### Doctor logs in but goes to profile setup

Check `/auth/doctor/me`. It should return:

```json
{
  "has_profile": true,
  "profile_id": 1
}
```

If `has_profile` is false, the doctor auth row is not linked to a doctor profile through `doctor_auth_id`.

### No booking slots appear

New doctor profiles now receive default slots. Also, requesting availability for an empty date auto-creates default slots for that doctor/date.

### Email is not delivered

Check:

- `ENABLE_EMAIL=true`
- `SMTP_HOST=smtp.gmail.com`
- `SMTP_PORT=587`
- `SMTP_USERNAME` is the sending Gmail address
- `SMTP_PASSWORD` is a Gmail app password
- `SMTP_FROM_EMAIL` matches the sender email

The API action still succeeds if SMTP fails.

### Frontend cannot call backend

Check:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Also confirm the backend is running on port `8000`.

---

## Hackathon Demo Script

1. Search `I have back pain` in `Lahore` with online consultation.
2. Confirm Orthopedic recommendations appear.
3. Open doctor profile.
4. Book appointment with patient email.
5. Try booking the same slot again and confirm conflict response.
6. Open unavailable doctor chatbot.
7. Submit name, email, and problem.
8. Open doctor dashboard.
9. Confirm appointment and chatbot lead are visible.
10. Show doctor-side assistant and logout.

---

## Development Rules

- Do not expose backend secrets in frontend code.
- Do not call Groq or SMTP directly from frontend.
- Do not introduce Supabase/Firebase/BaaS dependencies.
- Keep SQLite as the runtime database.
- Keep API endpoint paths and response keys stable.
- Keep doctor and patient experiences role-specific.
- Run backend tests and frontend build before handoff.
