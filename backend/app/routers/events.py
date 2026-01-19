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

# ==================== EVENT ROUTES ====================

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
    
    if event.creator_id != current_matcher.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this event"
        )
    
    return event

# PUBLIC ENDPOINT - No auth required
@router.get("/{event_id}/public", response_model=schemas.EventPublicResponse)
def get_event_public(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get public event info for participant registration (no auth required)."""
    event = crud.get_event_by_id(db, event_id)
    
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
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

# ==================== FORM QUESTION ROUTES ====================

@router.get("/{event_id}/form-questions", response_model=List[schemas.FormQuestionResponse])
def get_form_questions(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get all form questions for an event."""
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
    
    questions = crud.get_event_form_questions(db, event_id)
    return questions

# PUBLIC ENDPOINT - Get active questions for registration
@router.get("/{event_id}/form-questions/public", response_model=List[schemas.FormQuestionResponse])
def get_form_questions_public(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get active form questions for participant registration (no auth required)."""
    event = crud.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    questions = crud.get_active_form_questions(db, event_id)
    return questions

@router.post("/{event_id}/form-questions", response_model=schemas.FormQuestionResponse, status_code=status.HTTP_201_CREATED)
def create_form_question(
    event_id: int,
    question: schemas.FormQuestionCreate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Create a new form question."""
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
    
    db_question = crud.create_form_question(db, event_id, question)
    return db_question

@router.get("/{event_id}/form-questions/{question_id}", response_model=schemas.FormQuestionResponse)
def get_form_question(
    event_id: int,
    question_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get a specific form question."""
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
    
    question = crud.get_form_question_by_id(db, question_id)
    if not question or question.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question

@router.put("/{event_id}/form-questions/{question_id}", response_model=schemas.FormQuestionResponse)
def update_form_question(
    event_id: int,
    question_id: int,
    question_update: schemas.FormQuestionUpdate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Update a form question."""
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
    
    question = crud.get_form_question_by_id(db, question_id)
    if not question or question.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.is_standard:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify standard questions"
        )
    
    updated_question = crud.update_form_question(db, question_id, question_update)
    return updated_question

@router.delete("/{event_id}/form-questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_form_question(
    event_id: int,
    question_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Delete a form question."""
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
    
    question = crud.get_form_question_by_id(db, question_id)
    if not question or question.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.is_standard:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete standard questions"
        )
    
    crud.delete_form_question(db, question_id)
    return None

@router.put("/{event_id}/form-questions/reorder", status_code=status.HTTP_200_OK)
def reorder_form_questions(
    event_id: int,
    reorder_data: List[schemas.FormQuestionReorderItem],
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Reorder form questions."""
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
    
    crud.reorder_form_questions(db, event_id, reorder_data)
    return {"message": "Questions reordered successfully"}

# ==================== PARTICIPANT ROUTES ====================

# PUBLIC ENDPOINT - Participant registration (no auth required)
@router.post("/{event_id}/participants/register", response_model=schemas.ParticipantResponse, status_code=status.HTTP_201_CREATED)
def register_participant(
    event_id: int,
    participant: schemas.ParticipantRegister,
    db: Session = Depends(get_db)
):
    """Register a new participant for an event (public, no auth required)."""
    event = crud.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    if event.status != "registration_open":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration is not currently open for this event"
        )
    
    existing = crud.get_participant_by_email(db, event_id, participant.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered for this event"
        )
    
    if participant.age < 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must be at least 18 years old to register"
        )
    
    db_participant = crud.create_participant(db, event_id, participant)
    return db_participant

@router.get("/{event_id}/participants", response_model=List[schemas.ParticipantListResponse])
def get_participants(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get all participants for an event."""
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
    
    participants = crud.get_event_participants(db, event_id)
    return participants

@router.get("/{event_id}/participants/{participant_id}", response_model=schemas.ParticipantResponse)
def get_participant(
    event_id: int,
    participant_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get a specific participant."""
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
    
    participant = crud.get_participant_by_id(db, participant_id)
    if not participant or participant.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )
    
    return participant

@router.put("/{event_id}/participants/{participant_id}", response_model=schemas.ParticipantResponse)
def update_participant(
    event_id: int,
    participant_id: int,
    participant_update: schemas.ParticipantUpdate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Update a participant."""
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
    
    participant = crud.get_participant_by_id(db, participant_id)
    if not participant or participant.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )
    
    updated_participant = crud.update_participant(db, participant_id, participant_update)
    return updated_participant

@router.delete("/{event_id}/participants/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(
    event_id: int,
    participant_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Delete a participant."""
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
    
    participant = crud.get_participant_by_id(db, participant_id)
    if not participant or participant.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found"
        )
    
    crud.delete_participant(db, participant_id)
    return None

# ==================== VENUE ROUTES ====================

@router.get("/{event_id}/venues", response_model=List[schemas.VenueResponse])
def get_venues(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get all venues for an event."""
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
    
    venues = crud.get_event_venues(db, event_id)
    return venues

@router.post("/{event_id}/venues", response_model=schemas.VenueResponse, status_code=status.HTTP_201_CREATED)
def create_venue(
    event_id: int,
    venue: schemas.VenueCreate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Create a new venue for an event."""
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
    
    db_venue = crud.create_venue(db, event_id, venue)
    return db_venue

@router.get("/{event_id}/venues/{venue_id}", response_model=schemas.VenueResponse)
def get_venue(
    event_id: int,
    venue_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get a specific venue."""
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
    
    venue = crud.get_venue_by_id(db, venue_id)
    if not venue or venue.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    return venue

@router.put("/{event_id}/venues/{venue_id}", response_model=schemas.VenueResponse)
def update_venue(
    event_id: int,
    venue_id: int,
    venue_update: schemas.VenueUpdate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Update a venue."""
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
    
    venue = crud.get_venue_by_id(db, venue_id)
    if not venue or venue.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    updated_venue = crud.update_venue(db, venue_id, venue_update)
    return updated_venue

@router.delete("/{event_id}/venues/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venue(
    event_id: int,
    venue_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Delete a venue."""
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
    
    venue = crud.get_venue_by_id(db, venue_id)
    if not venue or venue.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venue not found"
        )
    
    crud.delete_venue(db, venue_id)
    return None

# ==================== MATCH ROUTES ====================

@router.get("/{event_id}/matches", response_model=List[schemas.MatchResponse])
def get_event_matches(
    event_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get all matches for an event."""
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

    matches = crud.get_event_matches(db, event_id)
    return matches

@router.post("/{event_id}/matches", response_model=schemas.MatchResponse, status_code=status.HTTP_201_CREATED)
def create_match(
    event_id: int,
    match: schemas.MatchCreate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Create a new match."""
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

    # Validate participants exist and belong to this event
    p1 = crud.get_participant_by_id(db, match.participant1_id)
    p2 = crud.get_participant_by_id(db, match.participant2_id)

    if not p1 or p1.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant 1 not found in this event"
        )

    if not p2 or p2.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant 2 not found in this event"
        )

    if match.participant1_id == match.participant2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot match a participant with themselves"
        )

    # Validate venue if provided
    if match.venue_id:
        venue = crud.get_venue_by_id(db, match.venue_id)
        if not venue or venue.event_id != event_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found in this event"
            )
        if venue.available_slots <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Venue has no available slots"
            )

    try:
        db_match = crud.create_match(db, event_id, match, current_matcher.id)
        return db_match
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/{event_id}/matches/{match_id}", response_model=schemas.MatchResponse)
def get_match(
    event_id: int,
    match_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Get a specific match."""
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

    match = crud.get_match_by_id(db, match_id)
    if not match or match.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    return match

@router.put("/{event_id}/matches/{match_id}", response_model=schemas.MatchResponse)
def update_match(
    event_id: int,
    match_id: int,
    match_update: schemas.MatchUpdate,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Update a match."""
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

    match = crud.get_match_by_id(db, match_id)
    if not match or match.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    # Validate venue if being updated
    if match_update.venue_id is not None:
        if match_update.venue_id:
            venue = crud.get_venue_by_id(db, match_update.venue_id)
            if not venue or venue.event_id != event_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Venue not found in this event"
                )

    updated_match = crud.update_match(db, match_id, match_update)
    if not updated_match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update match (venue may have no available slots)"
        )

    return updated_match

@router.delete("/{event_id}/matches/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(
    event_id: int,
    match_id: int,
    current_matcher: models.Matcher = Depends(get_current_matcher),
    db: Session = Depends(get_db)
):
    """Delete a match."""
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

    match = crud.get_match_by_id(db, match_id)
    if not match or match.event_id != event_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    crud.delete_match(db, match_id)
    return None