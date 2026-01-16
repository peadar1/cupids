from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import auth, crud, models
from .database import get_db

security = HTTPBearer()

def get_current_matcher(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.Matcher:
    """Get the current authenticated matcher from JWT token."""
    token = credentials.credentials
    
    # Decode token
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get matcher from database
    matcher_id = int(payload.get("sub"))
    matcher = crud.get_matcher_by_id(db, matcher_id)
    
    if not matcher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matcher not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return matcher