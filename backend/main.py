import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import chat, messages

app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

allowed_origins_env = os.getenv("ALLOWED_ORIGINS")
if allowed_origins_env:
    origins.extend([origin.strip() for origin in allowed_origins_env.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")
app.include_router(messages.router, prefix="/api")

# Optional Routers (require heavy dependencies like SQLAlchemy/Pgvector)
# These may fail to load on Vercel if deps are stripped to save size.
try:
    from backend.routers import scraper
    app.include_router(scraper.router, prefix="/api")
except ImportError:
    print("Warning: Scraper router not loaded (missing dependencies?)")

try:
    from backend.routers import ingestion
    app.include_router(ingestion.router, prefix="/api")
except ImportError:
    print("Warning: Ingestion router not loaded (missing dependencies?)")

# Core features - Must load or fail
from backend.routers import feedback, transcript
app.include_router(feedback.router, prefix="/api")
app.include_router(transcript.router, prefix="/api")

try:
    from backend.routers import admin
    app.include_router(admin.router, prefix="/api")
except ImportError:
    print("Warning: Admin router not loaded")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Hello from Backend!"}

