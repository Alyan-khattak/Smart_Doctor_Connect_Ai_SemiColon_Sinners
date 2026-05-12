from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Smart Doctor Connect AI"
    APP_ENV: str = "demo"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    DATABASE_URL: str = "sqlite:///./smart_doctor.db"

    GROQ_API_KEY: str | None = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_FROM_EMAIL: str = "sender_email"
    SMTP_FROM_NAME: str = "Smart Doctor Connect AI"
    
    APP_PUBLIC_URL: str = "http://localhost:8501"
    ENABLE_EMAIL: bool = True
    ENABLE_GROQ: bool = True

    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "*"

    JWT_SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440


settings = Settings()
