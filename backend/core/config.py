from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ibe160-chatbot"
    ALLOWED_ORIGINS: str = "*"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str  # Anon key for client-side
    SUPABASE_SERVICE_ROLE_KEY: str # For backend admin operations
    DATABASE_URL: str # Postgres connection string for SQLAlchemy
    GOOGLE_API_KEY: str # For Google Gemini AI

    class Config:
        env_file = ".env"

settings = Settings()
