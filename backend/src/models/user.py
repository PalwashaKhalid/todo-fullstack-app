from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """User model for authentication and task ownership"""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(SQLModel):
    """Schema for user registration"""
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)


class UserLogin(SQLModel):
    """Schema for user login"""
    email: str
    password: str


class UserResponse(SQLModel):
    """Schema for user response (excludes password)"""
    id: int
    email: str
    created_at: datetime
