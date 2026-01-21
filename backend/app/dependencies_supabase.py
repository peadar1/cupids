"""Dependencies for Supabase authentication"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from . import auth
from . import crud_supabase as crud
from .supabase_client import get_supabase_admin
from typing import Dict

security = HTTPBearer()

def get_current_matcher(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase_admin)
) -> Dict:
    """Get the current authenticated matcher from JWT token (Supabase version)."""
    token = credentials.credentials

    # Decode token
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get matcher email from token
    matcher_email = payload.get("sub")
    if not matcher_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get matcher from Supabase by email
    matcher = crud.get_matcher_by_email(supabase, matcher_email)

    if not matcher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Matcher not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return matcher
