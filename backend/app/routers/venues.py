from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..database import get_db
from ..dependencies import get_current_matcher

router = APIRouter(
    prefix="/api/events/{event_id}/venues",
    tags=["venues"]
)

def verify_event_access(event_id: int, current_matcher: models.Matcher, db: Session):
    """Verify that the current matcher has access to this event."""
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
    
    return event

@router.get("", response_model=List[schemas.VenueResponse])
def get_venues(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get all venues for an event."""
    verify_event_access(event_id, current_matcher, db)
    venues = crud.get_event_venues(db, event_id)
    return venues

@router.get("/{venue_id}", response_model=schemas.VenueResponse)
def get_venue(
    event_id: int,
    venue_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get a specific venue."""
    verify_event_access(event_id, current_matcher, db)
    
    venue = crud.get_venue_by_id(db, venue_id)
    if not venue or venue.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    return venue

@router.post("", response_model=schemas.VenueResponse, status_code=status.HTTP_201_CREATED)
def create_venue(
    event_id: int,
    venue: schemas.VenueCreate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Create a new venue for an event."""
    verify_event_access(event_id, current_matcher, db)
    db_venue = crud.create_venue(db, venue, event_id)
    return db_venue

@router.put("/{venue_id}", response_model=schemas.VenueResponse)
def update_venue(
    event_id: int,
    venue_id: int,
    venue_update: schemas.VenueUpdate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Update a venue."""
    verify_event_access(event_id, current_matcher, db)
    
    venue = crud.get_venue_by_id(db, venue_id)
    if not venue or venue.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    updated_venue = crud.update_venue(db, venue_id, venue_update)
    return updated_venue

@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venue(
    event_id: int,
    venue_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Delete a venue (soft delete)."""
    verify_event_access(event_id, current_matcher, db)
    
    venue = crud.get_venue_by_id(db, venue_id)
    if not venue or venue.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    crud.delete_venue(db, venue_id)
    return None