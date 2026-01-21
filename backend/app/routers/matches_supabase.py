"""Matches router using Supabase"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from typing import List, Dict
from .. import schemas
from .. import crud_supabase as crud
from ..supabase_client import get_supabase_admin
from ..dependencies_supabase import get_current_matcher

router = APIRouter(
    prefix="/api/events/{event_id}/matches",
    tags=["matches"]
)


@router.get("", response_model=List[schemas.MatchResponse])
def get_matches(
    event_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Get all matches for an event."""
    # Verify event access
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

    matches = crud.get_event_matches(supabase, event_id)
    return matches


@router.get("/{match_id}", response_model=schemas.MatchResponse)
def get_match(
    event_id: str,
    match_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Get a specific match by ID."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    match = crud.get_match_by_id(supabase, match_id)
    if not match or match['event_id'] != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    return match


@router.post("", response_model=schemas.MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(
    event_id: str,
    match: schemas.MatchCreate,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Create a new match."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    match_data = match.model_dump()
    db_match = crud.create_match(supabase, event_id, match_data, current_matcher['id'])
    return db_match


@router.put("/{match_id}", response_model=schemas.MatchResponse)
def update_match(
    event_id: str,
    match_id: str,
    match_update: schemas.MatchUpdate,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Update a match."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    match = crud.get_match_by_id(supabase, match_id)
    if not match or match['event_id'] != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    match_data = match_update.model_dump(exclude_unset=True)
    updated_match = crud.update_match(supabase, match_id, match_data)
    return updated_match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    event_id: str,
    match_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Delete a match."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    match = crud.get_match_by_id(supabase, match_id)
    if not match or match['event_id'] != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    crud.delete_match(supabase, match_id)
    return None
