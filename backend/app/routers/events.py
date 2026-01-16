from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_matcher

router = APIRouter(
    prefix="/api/events",
    tags=["events"]
)

@router.get("", response_model=List[schemas.EventListResponse])
def get_my_events(
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get all events for the current matcher."""
    events = crud.get_matcher_events(db, current_matcher.id)
    return events

@router.get("/{event_id}", response_model=schemas.EventResponse)
def get_event(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get a specific event by ID."""
    event = crud.get_event_by_id(db, event_id)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Check if matcher has access to this event
    if event.creator_id != current_matcher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )
    
    return event

@router.post("", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event: schemas.EventCreate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Create a new event."""
    db_event = crud.create_event(db, event, current_matcher.id)
    return db_event

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Update an event."""
    # Check if event exists and matcher has access
    event = crud.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.creator_id != current_matcher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )
    
    updated_event = crud.update_event(db, event_id, event_update)
    return updated_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Delete an event."""
    event = crud.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.creator_id != current_matcher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )
    
    crud.delete_event(db, event_id)
    return None