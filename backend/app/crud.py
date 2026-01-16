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