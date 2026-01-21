"""Auth router using Supabase"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from supabase import Client
from slowapi import Limiter
from slowapi.util import get_remote_address
from .. import schemas, auth
from .. import crud_supabase as crud
from ..supabase_client import get_supabase_admin

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", response_model=schemas.AuthResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
def signup(
    request: Request,
    matcher: schemas.MatcherCreate,
    supabase: Client = Depends(get_supabase_admin)
):
    """Register a new matcher. Rate limited to 5 signups per hour per IP."""
    # Check if email already exists
    existing_matcher = crud.get_matcher_by_email(supabase, matcher.email)
    if existing_matcher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new matcher
    matcher_data = matcher.model_dump()
    db_matcher = crud.create_matcher(supabase, matcher_data)

    # Create JWT token
    token = auth.create_access_token(data={"sub": db_matcher['email']})

    return {
        "access_token": token,
        "token_type": "bearer",
        "matcher": {
            "id": db_matcher['id'],
            "name": db_matcher['name'],
            "email": db_matcher['email'],
            "created_at": db_matcher['created_at'],
            "last_login": db_matcher.get('last_login')
        }
    }


@router.post("/login", response_model=schemas.AuthResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    credentials: schemas.MatcherLogin,
    supabase: Client = Depends(get_supabase_admin)
):
    """Login with email and password. Rate limited to 10 attempts per minute per IP."""
    matcher = crud.authenticate_matcher(supabase, credentials.email, credentials.password)

    if not matcher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    token = auth.create_access_token(data={"sub": matcher['email']})

    return {
        "access_token": token,
        "token_type": "bearer",
        "matcher": {
            "id": matcher['id'],
            "name": matcher['name'],
            "email": matcher['email'],
            "created_at": matcher['created_at'],
            "last_login": matcher.get('last_login')
        }
    }
