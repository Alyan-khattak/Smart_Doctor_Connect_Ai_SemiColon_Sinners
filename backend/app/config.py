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

    RESEND_API_KEY: str | None = None
    RESEND_FROM_EMAIL: str = "Smart Doctor Connect AI <onboarding@resend.dev>"
    RESEND_TEST_TO: str | None = None

    FRONTEND_URL: str = "http://localhost:3000"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"


settings = Settings()
