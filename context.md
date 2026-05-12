# Smart Doctor Connect AI — context.md

**Purpose:** Implementation history tracker. Updated after every meaningful change.  
**Project:** Smart Doctor Connect AI  
**Stack:** FastAPI + SQLAlchemy + SQLite + Groq + Resend + Next.js + Tailwind + Docker

---

## Project Understanding

### Documents Analyzed

| File | Purpose |
|---|---|
| `idea.md` | Product scope, features, API contracts, module definitions |
| `planning.md` | Build roadmap, DB schema, Docker, timeline |
| `schema.md` | SQLAlchemy models, Pydantic contracts, Supabase migration |
| `backend_agent.md` | FastAPI structure, API contracts, service patterns |
| `frontend_agent.md` | Next.js structure, TypeScript types, API client |
| `AGENTS.md` | Workflow rules, agent roles, commit gates |
| `demo.env` | Environment variable template |

### Core MVP Features

1. Doctor profiles (15 seeded doctors)
2. AI symptom → specialization via Groq
3. Doctor recommendation scoring
4. Conflict-free appointment booking
5. AI chatbot lead capture (when doctor unavailable)
6. Resend email notifications
7. Doctor dashboard
8. Docker-ready deployment

### Four Database Tables

- `doctors` — profiles
- `availability_slots` — bookable time slots
- `appointments` — booked appointments
- `chatbot_leads` — AI-collected patient details

---

## Change Log

---

### Entry 001

**Date/Time:** 2026-05-12 12:13 PKT  
**Module/Task:** Project Setup  
**File:** `context.md`  
**Change Type:** Added  
**Before:** File did not exist  
**After:** Created with full project understanding and change log format  
**Reason:** Required by user instructions as first step  
**Source Document:** User instructions  
**Contract Impact:** None  
**Testing Done:** N/A  
**Next Step:** Create backend folder structure and core files

---
