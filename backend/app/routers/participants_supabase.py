"""Participants router using Supabase"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from supabase import Client
from typing import List, Dict
from slowapi import Limiter
from slowapi.util import get_remote_address
from .. import schemas
from .. import crud_supabase as crud
from ..supabase_client import get_supabase_admin
from ..dependencies_supabase import get_current_matcher

router = APIRouter(
    prefix="/api/events/{event_id}/participants",
    tags=["participants"]
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=schemas.ParticipantResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour")
def register_participant(
    request: Request,
    event_id: str,
    participant: schemas.ParticipantRegister,
    supabase: Client = Depends(get_supabase_admin)
):
    """Public endpoint for participant registration. Rate limited to 3 registrations per hour per IP."""
    # Verify event exists
    event = crud.get_event_by_id(supabase, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    # Check if email is already registered for this event
    existing_participants = crud.get_event_participants(supabase, event_id)
    if any(p['email'].lower() == participant.email.lower() for p in existing_participants):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already registered for this event"
        )

    # Create participant
    participant_data = participant.model_dump()
    db_participant = crud.create_participant(supabase, event_id, participant_data)
    return db_participant


@router.get("", response_model=List[schemas.ParticipantListResponse])
def get_participants(
    event_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Get all participants for an event (requires auth)."""
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

    participants = crud.get_event_participants(supabase, event_id)
    return participants


@router.get("/{participant_id}", response_model=schemas.ParticipantResponse)
def get_participant(
    event_id: str,
    participant_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Get a specific participant by ID."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    participant = crud.get_participant_by_id(supabase, participant_id)
    if not participant or participant['event_id'] != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )

    return participant


@router.put("/{participant_id}", response_model=schemas.ParticipantResponse)
def update_participant(
    event_id: str,
    participant_id: str,
    participant_update: schemas.ParticipantUpdate,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Update a participant."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    participant = crud.get_participant_by_id(supabase, participant_id)
    if not participant or participant['event_id'] != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )

    participant_data = participant_update.model_dump(exclude_unset=True)
    updated_participant = crud.update_participant(supabase, participant_id, participant_data)
    return updated_participant


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(
    event_id: str,
    participant_id: str,
    current_matcher: Dict = Depends(get_current_matcher),
    supabase: Client = Depends(get_supabase_admin)
):
    """Delete a participant."""
    # Verify event access
    event = crud.get_event_by_id(supabase, event_id)
    if not event or event['creator_id'] != current_matcher['id']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )

    participant = crud.get_participant_by_id(supabase, participant_id)
    if not participant or participant['event_id'] != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )

    crud.delete_participant(supabase, participant_id)
    return None
