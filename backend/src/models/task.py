from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """Task model for todo items"""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(SQLModel):
    """Schema for task creation"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskUpdate(SQLModel):
    """Schema for task update"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)


class TaskStatusUpdate(SQLModel):
    """Schema for task status update"""
    completed: bool


class TaskResponse(SQLModel):
    """Schema for task response"""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
