from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, auth
from ..database import get_db
from datetime import timedelta

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)

@router.post("/signup", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(matcher: schemas.MatcherCreate, db: Session = Depends(get_db)):
    """Register a new matcher account."""
    print(f"🔍 Signup request received: {matcher.email}")
    
    # Check if email already exists
    existing_matcher = crud.get_matcher_by_email(db, matcher.email)
    if existing_matcher:
        print(f"❌ Email already exists: {matcher.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    print(f"✅ Creating new matcher...")
    # Create new matcher
    db_matcher = crud.create_matcher(db, matcher)
    print(f"✅ Matcher created with ID: {db_matcher.id}")
    
    print(f"🔑 Creating access token...")
    # Create access token
    access_token = auth.create_access_token(
        data={"sub": str(db_matcher.id), "email": db_matcher.email}
    )
    print(f"✅ Token created")
    
    print(f"📦 Preparing response...")
    response = {
        "access_token": access_token,
        "token_type": "bearer",
        "matcher": db_matcher
    }
    print(f"✅ Response prepared: {response}")
    
    return response

@router.post("/login", response_model=schemas.TokenResponse)
def login(credentials: schemas.MatcherLogin, db: Session = Depends(get_db)):
    """Login and get access token."""
    # Authenticate matcher
    matcher = crud.authenticate_matcher(db, credentials.email, credentials.password)
    if not matcher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = auth.create_access_token(
        data={"sub": str(matcher.id), "email": matcher.email}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "matcher": matcher
    }