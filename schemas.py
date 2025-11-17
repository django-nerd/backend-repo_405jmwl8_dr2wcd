from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Lead(BaseModel):
    company: str = Field(..., min_length=2, max_length=120)
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=40)
    message: Optional[str] = Field(None, max_length=2000)
    product: Optional[str] = Field(None, description="Requested product or interest area")

class Application(BaseModel):
    role: str = Field(..., min_length=2, max_length=120)
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=40)
    linkedin: Optional[str] = Field(None, max_length=200)
    portfolio: Optional[str] = Field(None, max_length=200)
    cover_letter: Optional[str] = Field(None, max_length=4000)

class FAQItem(BaseModel):
    question: str
    answer: str

class TeamMember(BaseModel):
    name: str
    title: str
    avatar: Optional[str] = None

class TimelineEvent(BaseModel):
    year: int
    title: str
    description: str

class TestResponse(BaseModel):
    backend: str
    database: str
    database_url: str
    database_name: str
    connection_status: str
    collections: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
