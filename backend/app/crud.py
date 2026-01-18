from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import Optional

# ==================== MATCHER CRUD ====================

def get_matcher_by_email(db: Session, email: str) -> Optional[models.Matcher]:
    """Get a matcher by email."""
    return db.query(models.Matcher).filter(models.Matcher.email == email).first()

def get_matcher_by_id(db: Session, matcher_id: int) -> Optional[models.Matcher]:
    """Get a matcher by ID."""
    return db.query(models.Matcher).filter(models.Matcher.id == matcher_id).first()

def create_matcher(db: Session, matcher: schemas.MatcherCreate) -> models.Matcher:
    """Create a new matcher."""
    hashed_password = auth.hash_password(matcher.password)
    db_matcher = models.Matcher(
        name=matcher.name,
        email=matcher.email,
        password_hash=hashed_password
    )
    db.add(db_matcher)
    db.commit()
    db.refresh(db_matcher)  # Get the ID and timestamps from DB
    return db_matcher

def authenticate_matcher(db: Session, email: str, password: str) -> Optional[models.Matcher]:
    """Authenticate a matcher by email and password."""
    matcher = get_matcher_by_email(db, email)
    if not matcher:
        return None
    if not auth.verify_password(password, matcher.password_hash):
        return None
    return matcher

# ==================== EVENT CRUD ====================

def get_event_by_id(db: Session, event_id: int) -> Optional[models.Event]:
    """Get an event by ID."""
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_matcher_events(db: Session, matcher_id: int) -> list[models.Event]:
    """Get all events created by or accessible to a matcher."""
    return db.query(models.Event).filter(models.Event.creator_id == matcher_id).all()

def create_event(db: Session, event: schemas.EventCreate, creator_id: int) -> models.Event:
    """Create a new event."""
    db_event = models.Event(
        name=event.name,
        description=event.description,
        event_date=event.event_date,
        creator_id=creator_id,
        status="setup",
        settings={}
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Also add creator to event_matchers table
    event_matcher = models.EventMatcher(
        event_id=db_event.id,
        matcher_id=creator_id,
        role="creator"
    )
    db.add(event_matcher)
    
    # Create default matching weights
    matching_weights = models.MatchingWeight(
        event_id=db_event.id
    )
    db.add(matching_weights)
    
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate) -> Optional[models.Event]:
    """Update an event."""
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return None
    
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int) -> bool:
    """Delete an event and all related data."""
    db_event = get_event_by_id(db, event_id)
    if not db_event:
        return False
    
    
    # Delete matching weights
    db.query(models.MatchingWeight).filter(
        models.MatchingWeight.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Delete event_matchers
    db.query(models.EventMatcher).filter(
        models.EventMatcher.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Delete form questions
    db.query(models.FormQuestion).filter(
        models.FormQuestion.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Delete venues
    db.query(models.Venue).filter(
        models.Venue.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Delete exclusions
    db.query(models.Exclusion).filter(
        models.Exclusion.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Delete matches
    db.query(models.Match).filter(
        models.Match.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Delete participants
    db.query(models.Participant).filter(
        models.Participant.event_id == event_id
    ).delete(synchronize_session=False)
    
    # Finally delete the event itself
    db.delete(db_event)
    db.commit()
    return True

# ==================== VENUE CRUD ====================

def get_venue_by_id(db: Session, venue_id: int) -> Optional[models.Venue]:
    """Get a venue by ID."""
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()

def get_event_venues(db: Session, event_id: int) -> list[models.Venue]:
    """Get all venues for an event."""
    return db.query(models.Venue).filter(
        models.Venue.event_id == event_id,
        models.Venue.is_active == True
    ).all()

def create_venue(db: Session, venue: schemas.VenueCreate, event_id: int) -> models.Venue:
    """Create a new venue for an event."""
    db_venue = models.Venue(
        event_id=event_id,
        name=venue.name,
        address=venue.address,
        total_capacity=venue.total_capacity,
        available_slots=venue.total_capacity,  # Initially all slots available
        min_age=venue.min_age,
        is_active=True
    )
    db.add(db_venue)
    db.commit()
    db.refresh(db_venue)
    return db_venue

def update_venue(db: Session, venue_id: int, venue_update: schemas.VenueUpdate) -> Optional[models.Venue]:
    """Update a venue."""
    db_venue = get_venue_by_id(db, venue_id)
    if not db_venue:
        return None
    
    update_data = venue_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_venue, field, value)
    
    db.commit()
    db.refresh(db_venue)
    return db_venue

def delete_venue(db: Session, venue_id: int) -> bool:
    """Soft delete a venue (set is_active to False)."""
    db_venue = get_venue_by_id(db, venue_id)
    if not db_venue:
        return False
    
    db_venue.is_active = False
    db.commit()
    return True