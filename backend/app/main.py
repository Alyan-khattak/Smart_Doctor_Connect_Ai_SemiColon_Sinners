from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routes import health, doctors, recommendations, availability, appointments, chatbot, email, dashboard

# Create all DB tables on startup (SQLite MVP)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Doctor Connect AI",
    description="AI-powered doctor discovery, appointment booking, and lead capture system for Pakistan.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(doctors.router)
app.include_router(recommendations.router)
app.include_router(availability.router)
app.include_router(appointments.router)
app.include_router(chatbot.router)
app.include_router(email.router)
app.include_router(dashboard.router)
