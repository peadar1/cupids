from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .routers import (
    auth_supabase as auth,
    events_supabase as events,
    venues_supabase as venues,
    participants_supabase as participants,
    form_questions_supabase as form_questions,
    matches_supabase as matches
)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Cupid's Matcher API",
    description="API for managing college cupids matching events",
    version="1.0.0"
)

# Get allowed CORS origins from environment variable
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

# CORS middleware with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(venues.router)
app.include_router(participants.router)
app.include_router(form_questions.router)
app.include_router(matches.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Cupid's Matcher API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
