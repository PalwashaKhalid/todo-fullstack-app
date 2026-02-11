# Data Model: Backend API & Data Layer

**Feature**: Backend API & Data Layer (002-backend-api-data)
**Date**: 2026-02-06
**Purpose**: Define SQLModel entity schemas for User and Task with validation rules, relationships, and database constraints

---

## Overview

This document defines the data models for the task management backend. The models use SQLModel (Pydantic + SQLAlchemy) for type-safe database operations with automatic validation.

**Key Principles:**
- User-Task relationship via foreign key (user_id)
- All queries filtered by authenticated user_id for data isolation
- Timestamps auto-managed (created_at, updated_at)
- Validation enforced at model level (title required, length limits)

---

## Entity: User

### Purpose
Represents an authenticated user in the system. Users are created by the authentication service (Better Auth) and referenced by tasks.

### Schema

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """
    User entity from authentication service.
    Minimal representation for task ownership.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2026-02-06T10:00:00Z"
            }
        }
```

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Primary key, auto-increment | Unique user identifier |
| email | str | Unique, indexed, max 255 chars | User email address |
| hashed_password | str | Max 255 chars | Bcrypt hashed password |
| created_at | datetime | Auto-set on creation | Account creation timestamp (UTC) |

### Indexes
- Primary key: `id` (auto-created)
- Unique index: `email` (for login lookups)

### Validation Rules
- Email must be unique across all users
- Email format validated by Pydantic
- Password stored as bcrypt hash (never plaintext)

### Notes
- User model managed by authentication service
- Backend only references user_id for task ownership
- No direct user CRUD operations in task API

---

## Entity: Task

### Purpose
Represents a to-do item belonging to a specific user. Tasks support CRUD operations with strict user ownership enforcement.

### Schema

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task entity with user ownership.
    All operations must filter by user_id for security.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "user_id": 456,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-02-06T10:30:00Z",
                "updated_at": "2026-02-06T10:30:00Z"
            }
        }
```

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | int | Primary key, auto-increment | Unique task identifier |
| user_id | int | Foreign key to users.id, indexed, not null | Task owner reference |
| title | str | Required, 1-200 chars | Task title/summary |
| description | str | Optional, max 2000 chars | Detailed task description |
| completed | bool | Default false | Task completion status |
| created_at | datetime | Auto-set on creation | Task creation timestamp (UTC) |
| updated_at | datetime | Auto-update on modification | Last modification timestamp (UTC) |

### Indexes
- Primary key: `id` (auto-created)
- Foreign key index: `user_id` (for filtering queries)
- Composite index: `(user_id, created_at)` (for sorted task lists)

### Validation Rules
- **Title**: Required, minimum 1 character, maximum 200 characters
- **Description**: Optional, maximum 2000 characters if provided
- **User ID**: Must reference existing user (foreign key constraint)
- **Completed**: Boolean, defaults to false
- **Timestamps**: Automatically managed, UTC timezone

### Relationships
- **User-Task**: Many-to-one (many tasks belong to one user)
- **Foreign Key**: `user_id` references `users.id`
- **Cascade**: ON DELETE CASCADE (when user deleted, their tasks are deleted)

### Query Patterns

**Create Task:**
```python
new_task = Task(
    user_id=current_user["id"],
    title="Buy groceries",
    description="Milk, eggs, bread"
)
db.add(new_task)
db.commit()
db.refresh(new_task)
```

**List User's Tasks:**
```python
statement = select(Task).where(
    Task.user_id == current_user["id"]
).order_by(Task.created_at.desc())
tasks = db.exec(statement).all()
```

**Get Specific Task (with ownership check):**
```python
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == current_user["id"]
)
task = db.exec(statement).first()
if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Update Task:**
```python
task.title = "Updated title"
task.updated_at = datetime.utcnow()
db.add(task)
db.commit()
db.refresh(task)
```

**Delete Task:**
```python
db.delete(task)
db.commit()
```

---

## Request/Response Schemas

### TaskCreate (Request)

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }
```

### TaskUpdate (Request)

```python
class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "description": "Milk, eggs, bread, chicken"
            }
        }
```

### TaskStatusUpdate (Request)

```python
class TaskStatusUpdate(BaseModel):
    """Request schema for toggling task completion status."""
    completed: bool

    class Config:
        schema_extra = {
            "example": {
                "completed": True
            }
        }
```

### TaskResponse (Response)

```python
class TaskResponse(BaseModel):
    """Response schema for task data."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "user_id": 456,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-02-06T10:30:00Z",
                "updated_at": "2026-02-06T10:30:00Z"
            }
        }
```

---

## Database Migrations

### Initial Schema Creation

```sql
-- Users table (managed by auth service)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

### SQLModel Auto-Creation

```python
from sqlmodel import SQLModel, create_engine

# Create all tables
engine = create_engine(database_url)
SQLModel.metadata.create_all(engine)
```

---

## Validation Examples

### Valid Task Creation
```python
# Valid: Title within limits
task = TaskCreate(title="Buy groceries", description="Milk, eggs")
# ✅ Passes validation

# Valid: Title at maximum length
task = TaskCreate(title="x" * 200, description="Test")
# ✅ Passes validation

# Valid: No description
task = TaskCreate(title="Quick task")
# ✅ Passes validation (description optional)
```

### Invalid Task Creation
```python
# Invalid: Empty title
task = TaskCreate(title="", description="Test")
# ❌ ValidationError: title must be at least 1 character

# Invalid: Title too long
task = TaskCreate(title="x" * 201, description="Test")
# ❌ ValidationError: title must be at most 200 characters

# Invalid: Description too long
task = TaskCreate(title="Test", description="x" * 2001)
# ❌ ValidationError: description must be at most 2000 characters

# Invalid: Missing title
task = TaskCreate(description="Test")
# ❌ ValidationError: title is required
```

---

## Security Considerations

### Data Isolation
- **All queries MUST filter by user_id**: `Task.user_id == current_user["id"]`
- **Never trust user_id from request**: Always use user_id from JWT token
- **Authorization checks**: Verify task ownership before update/delete operations

### SQL Injection Prevention
- SQLModel uses parameterized queries automatically
- Never concatenate user input into SQL strings
- Use SQLModel's query builder for all database operations

### Timestamp Handling
- All timestamps stored in UTC
- `created_at` set once on creation
- `updated_at` updated on every modification
- Frontend responsible for timezone conversion

---

## Summary

**Entities Defined:**
- User: Minimal representation for task ownership
- Task: Full CRUD entity with user ownership

**Key Features:**
- Type-safe models with Pydantic validation
- Automatic timestamp management
- Foreign key constraints for data integrity
- Indexes optimized for common query patterns
- Request/response schemas for API contracts

**Security:**
- All queries filtered by authenticated user_id
- Foreign key constraints prevent orphaned tasks
- Validation enforced at model level

**Status**: ✅ Data models ready for implementation
