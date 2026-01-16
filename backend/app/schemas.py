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