"""Dependencies for Supabase authentication"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import Client
from . import auth
from . import crud_supabase as crud
from .supabase_client import get_supabase_admin
from typing import Dict, Tuple

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


def verify_event_ownership(
    event_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
) -> Tuple[Dict, Dict]:
    """Verify that the current matcher owns the specified event.

    Returns:
        Tuple of (event, current_matcher) if authorized.

    Raises:
        HTTPException: 404 if event not found, 403 if not authorized.
    """
    event = crud.get_event_by_id(supabase, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    return event, current_matcher
