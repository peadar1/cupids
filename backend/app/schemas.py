from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date

# ==================== MATCHER SCHEMAS ====================

class MatcherBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class MatcherCreate(MatcherBase):
    password: str = Field(..., min_length=8, max_length=100)

class MatcherLogin(BaseModel):
    email: EmailStr
    password: str

class MatcherResponse(MatcherBase):
    id: str  # UUID from Supabase
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    matcher: MatcherResponse

# Alias for compatibility
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    matcher: MatcherResponse

# ==================== EVENT SCHEMAS ====================

class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: date

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    event_date: Optional[date] = None
    status: Optional[str] = None
    settings: Optional[dict] = None

class EventResponse(EventBase):
    id: str  # UUID from Supabase
    creator_id: str  # UUID from Supabase
    status: str
    settings: Optional[dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class EventListResponse(BaseModel):
    id: str  # UUID from Supabase
    name: str
    event_date: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Public event response (limited info for participants)
class EventPublicResponse(BaseModel):
    id: str  # UUID from Supabase
    name: str
    description: Optional[str] = None
    event_date: date
    status: str
    settings: Optional[dict] = None  # Include settings for form configuration

    model_config = ConfigDict(from_attributes=True)

# ==================== PARTICIPANT SCHEMAS ====================

class ParticipantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    age: int = Field(..., ge=18, le=100)
    gender: str = Field(..., pattern="^(male|female|non_binary|other)$")
    interested_in: str = Field(..., pattern="^(male|female|everyone)$")
    bio: Optional[str] = Field(None, max_length=500)

# For public registration (no auth required)
class ParticipantRegister(ParticipantBase):
    form_answers: Optional[dict] = {}  # Custom question answers

# For creating participant (admin)
class ParticipantCreate(ParticipantBase):
    form_answers: Optional[dict] = {}

# For updating participant
class ParticipantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    age: Optional[int] = Field(None, ge=18, le=100)
    gender: Optional[str] = Field(None, pattern="^(male|female|non_binary|other)$")
    interested_in: Optional[str] = Field(None, pattern="^(male|female|everyone)$")
    bio: Optional[str] = Field(None, max_length=500)
    status: Optional[str] = Field(None, pattern="^(registered|matched|withdrawn|waitlisted)$")
    form_answers: Optional[dict] = None

class ParticipantResponse(BaseModel):
    id: str  # UUID from Supabase
    event_id: str  # UUID from Supabase
    name: str
    email: str
    phone_number: Optional[str] = None
    age: int
    form_answers: dict
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ParticipantListResponse(BaseModel):
    id: str  # UUID from Supabase
    name: str
    email: str
    age: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ==================== VENUE SCHEMAS ====================

class VenueBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: Optional[str] = None
    total_capacity: int = Field(..., ge=1)
    min_age: int = Field(..., ge=18, le=21)

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = None
    total_capacity: Optional[int] = Field(None, ge=1)
    min_age: Optional[int] = Field(None, ge=18, le=21)
    is_active: Optional[bool] = None

class VenueResponse(VenueBase):
    id: str  # UUID from Supabase
    event_id: str  # UUID from Supabase
    available_slots: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# ==================== FORM QUESTION SCHEMAS ====================

class FormQuestionBase(BaseModel):
    question_key: str = Field(..., min_length=1, max_length=50)
    question_text: str = Field(..., min_length=1, max_length=500)
    question_type: str = Field(..., pattern="^(text|textarea|select|multi_select|checkbox|radio|number|email|phone|date)$")
    options: Optional[List[str]] = None
    is_required: bool = True
    is_active: bool = True

class FormQuestionCreate(FormQuestionBase):
    display_order: Optional[int] = None

class FormQuestionUpdate(BaseModel):
    question_key: Optional[str] = Field(None, min_length=1, max_length=50)
    question_text: Optional[str] = Field(None, min_length=1, max_length=500)
    question_type: Optional[str] = Field(None, pattern="^(text|textarea|select|multi_select|checkbox|radio|number|email|phone|date)$")
    options: Optional[List[str]] = None
    is_required: Optional[bool] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None

class FormQuestionResponse(FormQuestionBase):
    id: str  # UUID from Supabase
    event_id: str  # UUID from Supabase
    is_standard: bool
    display_order: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class FormQuestionReorderItem(BaseModel):
    id: str  # UUID from Supabase
    display_order: int

class FormQuestionReorder(BaseModel):
    questions: List[FormQuestionReorderItem]

# ==================== MATCH SCHEMAS ====================

class MatchBase(BaseModel):
    participant1_id: str  # UUID from Supabase
    participant2_id: str  # UUID from Supabase
    compatibility_score: int = Field(..., ge=0, le=100)
    venue_id: Optional[str] = None  # UUID from Supabase
    notes: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(BaseModel):
    compatibility_score: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = None
    venue_id: Optional[str] = None  # UUID from Supabase
    notes: Optional[str] = None

class ParticipantMinimal(BaseModel):
    id: str  # UUID from Supabase
    name: str
    age: int
    gender: str

    model_config = ConfigDict(from_attributes=True)

class MatchResponse(BaseModel):
    id: str  # UUID from Supabase
    event_id: str  # UUID from Supabase
    participant1_id: str  # UUID from Supabase
    participant2_id: str  # UUID from Supabase
    compatibility_score: int
    status: str
    venue_id: Optional[str] = None  # UUID from Supabase
    matched_by: str  # UUID from Supabase
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)