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