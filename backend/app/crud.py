from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas, auth
from typing import Optional, List

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
    db.refresh(db_matcher)
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

def get_matcher_events(db: Session, matcher_id: int) -> List[models.Event]:
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
    
    # Add creator to event_matchers table
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

# ==================== PARTICIPANT CRUD ====================

def get_participant_by_id(db: Session, participant_id: int) -> Optional[models.Participant]:
    """Get a participant by ID."""
    return db.query(models.Participant).filter(models.Participant.id == participant_id).first()

def get_participant_by_email(db: Session, event_id: int, email: str) -> Optional[models.Participant]:
    """Get a participant by email for a specific event."""
    return db.query(models.Participant).filter(
        models.Participant.event_id == event_id,
        models.Participant.email == email
    ).first()

def get_event_participants(db: Session, event_id: int) -> List[models.Participant]:
    """Get all participants for an event."""
    return db.query(models.Participant).filter(
        models.Participant.event_id == event_id
    ).order_by(models.Participant.created_at.desc()).all()

def create_participant(db: Session, event_id: int, participant: schemas.ParticipantRegister) -> models.Participant:
    """Create a new participant (public registration)."""
    # Build form_answers from the registration data
    form_answers = {
        "gender": participant.gender,
        "interested_in": participant.interested_in,
        "bio": participant.bio or "",
        "date_of_birth": str(participant.date_of_birth) if participant.date_of_birth else None,
        **(participant.form_answers or {})  # Include custom question answers
    }
    
    db_participant = models.Participant(
        event_id=event_id,
        name=participant.name,
        email=participant.email,
        phone_number=participant.phone,
        age=participant.age,
        form_answers=form_answers,
        status="registered"
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def update_participant(db: Session, participant_id: int, participant_update: schemas.ParticipantUpdate) -> Optional[models.Participant]:
    """Update a participant."""
    db_participant = get_participant_by_id(db, participant_id)
    if not db_participant:
        return None
    
    update_data = participant_update.model_dump(exclude_unset=True)
    
    # Handle phone field mapping
    if 'phone' in update_data:
        update_data['phone_number'] = update_data.pop('phone')
    
    for field, value in update_data.items():
        setattr(db_participant, field, value)
    
    db.commit()
    db.refresh(db_participant)
    return db_participant

def delete_participant(db: Session, participant_id: int) -> bool:
    """Delete a participant."""
    db_participant = get_participant_by_id(db, participant_id)
    if not db_participant:
        return False
    
    # Delete related exclusions
    db.query(models.Exclusion).filter(
        models.Exclusion.participant_id == participant_id
    ).delete(synchronize_session=False)
    
    # Delete related matches
    db.query(models.Match).filter(
        (models.Match.participant1_id == participant_id) | 
        (models.Match.participant2_id == participant_id)
    ).delete(synchronize_session=False)
    
    db.delete(db_participant)
    db.commit()
    return True

# ==================== VENUE CRUD ====================

def get_venue_by_id(db: Session, venue_id: int) -> Optional[models.Venue]:
    """Get a venue by ID."""
    return db.query(models.Venue).filter(models.Venue.id == venue_id).first()

def get_event_venues(db: Session, event_id: int) -> List[models.Venue]:
    """Get all venues for an event."""
    return db.query(models.Venue).filter(
        models.Venue.event_id == event_id
    ).order_by(models.Venue.name).all()

def create_venue(db: Session, event_id: int, venue: schemas.VenueCreate) -> models.Venue:
    """Create a new venue."""
    db_venue = models.Venue(
        event_id=event_id,
        name=venue.name,
        address=venue.address,
        total_capacity=venue.total_capacity,
        available_slots=venue.total_capacity,
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
    
    # If total_capacity is updated, adjust available_slots proportionally
    if 'total_capacity' in update_data:
        old_capacity = db_venue.total_capacity
        new_capacity = update_data['total_capacity']
        used_slots = old_capacity - db_venue.available_slots
        update_data['available_slots'] = max(0, new_capacity - used_slots)
    
    for field, value in update_data.items():
        setattr(db_venue, field, value)
    
    db.commit()
    db.refresh(db_venue)
    return db_venue

def delete_venue(db: Session, venue_id: int) -> bool:
    """Delete a venue."""
    db_venue = get_venue_by_id(db, venue_id)
    if not db_venue:
        return False
    
    # Check if venue has matches assigned
    matches_count = db.query(models.Match).filter(
        models.Match.venue_id == venue_id
    ).count()
    
    if matches_count > 0:
        # Just deactivate instead of deleting
        db_venue.is_active = False
        db.commit()
        return True
    
    db.delete(db_venue)
    db.commit()
    return True

# ==================== FORM QUESTION CRUD ====================

def get_form_question_by_id(db: Session, question_id: int) -> Optional[models.FormQuestion]:
    """Get a form question by ID."""
    return db.query(models.FormQuestion).filter(models.FormQuestion.id == question_id).first()

def get_event_form_questions(db: Session, event_id: int) -> List[models.FormQuestion]:
    """Get all form questions for an event."""
    return db.query(models.FormQuestion).filter(
        models.FormQuestion.event_id == event_id
    ).order_by(models.FormQuestion.is_standard.desc(), models.FormQuestion.display_order).all()

def get_active_form_questions(db: Session, event_id: int) -> List[models.FormQuestion]:
    """Get all active (non-standard) form questions for an event."""
    return db.query(models.FormQuestion).filter(
        models.FormQuestion.event_id == event_id,
        models.FormQuestion.is_active == True,
        models.FormQuestion.is_standard == False
    ).order_by(models.FormQuestion.display_order).all()

def get_next_display_order(db: Session, event_id: int) -> int:
    """Get the next display order for a new question."""
    max_order = db.query(models.FormQuestion).filter(
        models.FormQuestion.event_id == event_id,
        models.FormQuestion.is_standard == False
    ).count()
    return max_order + 1

def create_form_question(db: Session, event_id: int, question: schemas.FormQuestionCreate) -> models.FormQuestion:
    """Create a new form question."""
    display_order = question.display_order or get_next_display_order(db, event_id)
    
    db_question = models.FormQuestion(
        event_id=event_id,
        question_key=question.question_key,
        question_text=question.question_text,
        question_type=question.question_type,
        options=question.options,
        is_required=question.is_required,
        is_standard=False,  # Custom questions are never standard
        is_active=question.is_active,
        display_order=display_order
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def update_form_question(db: Session, question_id: int, question_update: schemas.FormQuestionUpdate) -> Optional[models.FormQuestion]:
    """Update a form question."""
    db_question = get_form_question_by_id(db, question_id)
    if not db_question:
        return None
    
    # Don't allow updating standard questions
    if db_question.is_standard:
        return None
    
    update_data = question_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_form_question(db: Session, question_id: int) -> bool:
    """Delete a form question."""
    db_question = get_form_question_by_id(db, question_id)
    if not db_question:
        return False
    
    # Don't allow deleting standard questions
    if db_question.is_standard:
        return False
    
    db.delete(db_question)
    db.commit()
    return True

def reorder_form_questions(db: Session, event_id: int, reorder_data: List[schemas.FormQuestionReorderItem]) -> bool:
    """Reorder form questions."""
    for item in reorder_data:
        db_question = get_form_question_by_id(db, item.id)
        if db_question and db_question.event_id == event_id and not db_question.is_standard:
            db_question.display_order = item.display_order

    db.commit()
    return True

# ==================== MATCH CRUD ====================

def get_match_by_id(db: Session, match_id: int) -> Optional[models.Match]:
    """Get a match by ID."""
    return db.query(models.Match).filter(models.Match.id == match_id).first()

def get_event_matches(db: Session, event_id: int) -> List[models.Match]:
    """Get all matches for an event."""
    return db.query(models.Match).filter(models.Match.event_id == event_id).all()

def create_match(db: Session, event_id: int, match: schemas.MatchCreate, matcher_id: int) -> models.Match:
    """Create a new match."""
    # Ensure participant1_id < participant2_id
    p1_id = min(match.participant1_id, match.participant2_id)
    p2_id = max(match.participant1_id, match.participant2_id)

    db_match = models.Match(
        event_id=event_id,
        participant1_id=p1_id,
        participant2_id=p2_id,
        compatibility_score=match.compatibility_score,
        venue_id=match.venue_id,
        matched_by=matcher_id,
        notes=match.notes,
        status="pending"
    )
    db.add(db_match)

    # If venue is assigned, reduce available slots
    if match.venue_id:
        venue = get_venue_by_id(db, match.venue_id)
        if venue and venue.available_slots > 0:
            venue.available_slots -= 1
            db_match.venue_assigned_at = func.now()

    db.commit()
    db.refresh(db_match)
    return db_match

def update_match(db: Session, match_id: int, match_update: schemas.MatchUpdate) -> Optional[models.Match]:
    """Update a match."""
    db_match = get_match_by_id(db, match_id)
    if not db_match:
        return None

    update_data = match_update.model_dump(exclude_unset=True)

    # Handle venue reassignment
    if 'venue_id' in update_data:
        old_venue_id = db_match.venue_id
        new_venue_id = update_data['venue_id']

        # Free up old venue slot
        if old_venue_id:
            old_venue = get_venue_by_id(db, old_venue_id)
            if old_venue:
                old_venue.available_slots += 1

        # Reserve new venue slot
        if new_venue_id:
            new_venue = get_venue_by_id(db, new_venue_id)
            if new_venue and new_venue.available_slots > 0:
                new_venue.available_slots -= 1
                update_data['venue_assigned_at'] = func.now()
            else:
                return None  # No slots available
        else:
            update_data['venue_assigned_at'] = None

    for field, value in update_data.items():
        setattr(db_match, field, value)

    db.commit()
    db.refresh(db_match)
    return db_match

def delete_match(db: Session, match_id: int) -> bool:
    """Delete a match."""
    db_match = get_match_by_id(db, match_id)
    if not db_match:
        return False

    # Free up venue slot if assigned
    if db_match.venue_id:
        venue = get_venue_by_id(db, db_match.venue_id)
        if venue:
            venue.available_slots += 1

    db.delete(db_match)
    db.commit()
    return True