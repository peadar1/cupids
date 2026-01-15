from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, JSON, ForeignKey, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base


# 1. MATCHERS TABLE
class Matcher(Base):
    __tablename__ = "matchers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    created_events = relationship("Event", back_populates="creator")
    event_memberships = relationship("EventMatcher", back_populates="matcher")
    matches_created = relationship("Match", back_populates="matcher")


# 2. EVENTS TABLE
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey("matchers.id"), nullable=False)
    event_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="setup")  # setup, registration_open, matching_in_progress, completed, cancelled
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    creator = relationship("Matcher", back_populates="created_events")
    matchers = relationship("EventMatcher", back_populates="event")
    participants = relationship("Participant", back_populates="event")
    form_questions = relationship("FormQuestion", back_populates="event")
    matches = relationship("Match", back_populates="event")
    venues = relationship("Venue", back_populates="event")
    matching_weights = relationship("MatchingWeight", back_populates="event", uselist=False)


# 3. EVENT_MATCHERS TABLE (Many-to-Many)
class EventMatcher(Base):
    __tablename__ = "event_matchers"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    matcher_id = Column(Integer, ForeignKey("matchers.id"), nullable=False)
    role = Column(String, nullable=False)  # creator, matcher, viewer
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="matchers")
    matcher = relationship("Matcher", back_populates="event_memberships")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('event_id', 'matcher_id', name='unique_event_matcher'),
    )

# 4. FORM_QUESTIONS TABLE
class FormQuestion(Base):
    __tablename__ = "form_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    question_key = Column(String, nullable=False)  # e.g., "year", "course", "interests"
    question_text = Column(String, nullable=False)
    question_type = Column(String, nullable=False)  # text, textarea, select, multi_select, checkbox, radio, number, email, phone
    options = Column(JSON, nullable=True)  # For select/checkbox options
    is_required = Column(Boolean, default=True)
    is_standard = Column(Boolean, default=False)  # True for name, email, age, etc.
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="form_questions")
    
    # Indexes
    __table_args__ = (
        Index('idx_event_questions', 'event_id', 'is_active'),
    )


# 5. PARTICIPANTS TABLE
class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone_number = Column(String, nullable=True)
    age = Column(Integer, nullable=False)
    form_answers = Column(JSON, nullable=False)  # All form question answers
    status = Column(String, nullable=False, default="registered")  # registered, matched, withdrawn, waitlisted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="participants")
    matches_as_p1 = relationship("Match", foreign_keys="Match.participant1_id", back_populates="participant1")
    matches_as_p2 = relationship("Match", foreign_keys="Match.participant2_id", back_populates="participant2")
    exclusions = relationship("Exclusion", back_populates="participant")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('event_id', 'email', name='unique_event_email'),
        Index('idx_event_participants', 'event_id', 'status'),
    )


# 6. EXCLUSIONS TABLE
class Exclusion(Base):
    __tablename__ = "exclusions"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    excluded_name = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    event = relationship("Event")
    participant = relationship("Participant", back_populates="exclusions")


# 7. MATCHES TABLE
class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    participant1_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    participant2_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    compatibility_score = Column(Integer, nullable=False)  # 0-100
    status = Column(String, nullable=False, default="pending")  # pending, approved, notified, confirmed
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=True)
    venue_assigned_at = Column(DateTime(timezone=True), nullable=True)
    matched_by = Column(Integer, ForeignKey("matchers.id"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="matches")
    participant1 = relationship("Participant", foreign_keys=[participant1_id], back_populates="matches_as_p1")
    participant2 = relationship("Participant", foreign_keys=[participant2_id], back_populates="matches_as_p2")
    venue = relationship("Venue", back_populates="matches")
    matcher = relationship("Matcher", back_populates="matches_created")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('participant1_id < participant2_id', name='check_participant_order'),
        UniqueConstraint('event_id', 'participant1_id', 'participant2_id', name='unique_match_pair'),
        Index('idx_event_matches', 'event_id', 'status'),
    )


# 8. VENUES TABLE
class Venue(Base):
    __tablename__ = "venues"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    total_capacity = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    min_age = Column(Integer, nullable=False)  # 18 or 21
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="venues")
    matches = relationship("Match", back_populates="venue")


# 9. MATCHING_WEIGHTS TABLE
class MatchingWeight(Base):
    __tablename__ = "matching_weights"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, unique=True)
    age_gap_weight = Column(Integer, default=30)
    same_year_weight = Column(Integer, default=25)
    interests_weight = Column(Integer, default=20)
    personality_weight = Column(Integer, default=15)
    different_course_weight = Column(Integer, default=10)
    music_taste_weight = Column(Integer, default=5)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    event = relationship("Event", back_populates="matching_weights")