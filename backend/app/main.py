from fastapi import FastAPI
from .database import engine, Base
from . import models

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Cupid's Matcher API",
    description="API for managing college cupids matching events",
    version="1.0.0"
)

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