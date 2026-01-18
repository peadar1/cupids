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
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
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

class EventResponse(EventBase):
    id: int
    creator_id: int
    status: str
    settings: Optional[dict] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class EventListResponse(BaseModel):
    id: int
    name: str
    event_date: date
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# ==================== VENUE SCHEMAS ====================

class VenueBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: Optional[str] = None
    total_capacity: int = Field(..., gt=0)
    min_age: int = Field(..., ge=18, le=21)  # Must be 18 or 21

class VenueCreate(VenueBase):
    pass

class VenueUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = None
    total_capacity: Optional[int] = Field(None, gt=0)
    available_slots: Optional[int] = Field(None, ge=0)
    min_age: Optional[int] = Field(None, ge=18, le=21)
    is_active: Optional[bool] = None

class VenueResponse(VenueBase):
    id: int
    event_id: int
    available_slots: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)