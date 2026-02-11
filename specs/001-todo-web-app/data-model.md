# Data Model: Todo Full-Stack Web Application

**Feature**: 001-todo-web-app
**Date**: 2026-02-06
**Phase**: Phase 1 - Database Schema Design

## Overview

This document defines the database schema for the Todo Full-Stack Web Application. The schema supports multi-user authentication and task management with strict data isolation between users. All tables use PostgreSQL via Neon Serverless with SQLModel ORM for type-safe operations.

## Entity Relationship Diagram

```
┌─────────────────────────┐
│        users            │
│─────────────────────────│
│ id (PK)        INTEGER  │
│ email (UK)     VARCHAR  │◄──────────┐
│ hashed_password VARCHAR │           │
│ created_at     TIMESTAMP│           │
└─────────────────────────┘           │
                                      │ 1:N
                                      │
                          ┌───────────┴──────────────┐
                          │        tasks             │
                          │──────────────────────────│
                          │ id (PK)        INTEGER   │
                          │ user_id (FK)   INTEGER   │
                          │ title          VARCHAR   │
                          │ description    TEXT      │
                          │ completed      BOOLEAN   │
                          │ created_at     TIMESTAMP │
                          │ updated_at     TIMESTAMP │
                          └──────────────────────────┘
```

## Entities

### Entity: User

**Purpose**: Represents an individual user account in the system.

**Table Name**: `users`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for login) |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt-hashed password (never store plaintext) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp (UTC) |

**Indexes**:
- PRIMARY KEY on `id` (automatic)
- UNIQUE INDEX on `email` (for fast login lookups and duplicate prevention)

**Relationships**:
- One user has many tasks (1:N relationship)

**Validation Rules**:
- Email must be valid format (validated by Pydantic before database insert)
- Email must be unique (enforced by database constraint)
- Password must be hashed with bcrypt before storage (minimum 8 characters validated at API layer)
- created_at is immutable after creation

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Security Considerations**:
- Password field is named `hashed_password` to prevent accidental plaintext storage
- Email is indexed for fast authentication lookups
- created_at provides audit trail for account creation

---

### Entity: Task

**Purpose**: Represents a todo item belonging to a specific user.

**Table Name**: `tasks`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the task |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner of the task (enforces data isolation) |
| title | VARCHAR(200) | NOT NULL | Task title (required, max 200 characters) |
| description | TEXT | NULL | Optional detailed description of the task |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Task completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification timestamp (UTC) |

**Indexes**:
- PRIMARY KEY on `id` (automatic)
- INDEX on `user_id` (for fast filtering by owner)
- COMPOSITE INDEX on `(user_id, created_at)` (for sorted queries)

**Relationships**:
- Many tasks belong to one user (N:1 relationship)
- Foreign key constraint ensures referential integrity

**Validation Rules**:
- title must not be empty (validated at API layer)
- title maximum length 200 characters
- description maximum length 2000 characters (validated at API layer)
- user_id must reference existing user (enforced by foreign key)
- completed defaults to false for new tasks
- updated_at automatically updated on modification

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Security Considerations**:
- user_id is indexed for fast filtering (critical for data isolation)
- All queries MUST filter by user_id to prevent cross-user data access
- Foreign key constraint prevents orphaned tasks

---

## Database Constraints

### Foreign Key Constraints

```sql
ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

**Rationale**: When a user is deleted, all their tasks are automatically deleted (CASCADE). This maintains referential integrity and prevents orphaned tasks.

### Unique Constraints

```sql
ALTER TABLE users
ADD CONSTRAINT uk_users_email
UNIQUE (email);
```

**Rationale**: Ensures each email address can only be used for one account.

---

## Index Strategy

### Performance Indexes

**users.email (UNIQUE INDEX)**:
- **Purpose**: Fast authentication lookups during signin
- **Query**: `SELECT * FROM users WHERE email = ?`
- **Impact**: O(log n) lookup instead of O(n) table scan

**tasks.user_id (INDEX)**:
- **Purpose**: Fast filtering of tasks by owner
- **Query**: `SELECT * FROM tasks WHERE user_id = ?`
- **Impact**: Critical for data isolation, enables fast user-specific queries

**tasks.(user_id, created_at) (COMPOSITE INDEX)**:
- **Purpose**: Fast sorted queries for user's tasks
- **Query**: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
- **Impact**: Eliminates need for separate sort operation

### Index Maintenance

- Indexes are automatically maintained by PostgreSQL
- Neon autoscaling handles index performance
- No manual index rebuilding required

---

## Data Isolation Strategy

### Query Filtering Pattern

**CRITICAL**: Every query on the `tasks` table MUST include `WHERE user_id = ?` filter.

**Correct Pattern**:
```python
# Get user's tasks
tasks = session.exec(
    select(Task).where(Task.user_id == current_user.id)
).all()

# Update user's task
task = session.exec(
    select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
).first()
```

**Incorrect Pattern (SECURITY VULNERABILITY)**:
```python
# WRONG: Returns all tasks from all users
tasks = session.exec(select(Task)).all()

# WRONG: Allows access to other users' tasks
task = session.exec(
    select(Task).where(Task.id == task_id)
).first()
```

### Authorization Checks

**Before UPDATE or DELETE operations**:
1. Query task with both `id` and `user_id` filters
2. If task not found, return 404 Not Found
3. If task belongs to different user, return 403 Forbidden
4. Only proceed if task belongs to authenticated user

---

## Migration Strategy

### Initial Schema Creation

```sql
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create index on email
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Create tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create indexes on tasks
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_id_created_at ON tasks(user_id, created_at);
```

### SQLModel Auto-Migration

SQLModel can automatically create tables from model definitions:

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

**Note**: For production, use proper migration tools (Alembic) for version control and rollback capability.

---

## Data Retention

### User Data
- User accounts persist indefinitely
- No automatic deletion or archiving
- Users can request account deletion (future feature)

### Task Data
- Tasks persist indefinitely
- No automatic deletion or archiving
- Tasks are deleted when user account is deleted (CASCADE)

---

## Backup and Recovery

### Neon Platform Features
- Automatic backups managed by Neon
- Point-in-time recovery available
- Database branching for testing

### Application-Level Considerations
- No application-level backup logic required
- Rely on Neon platform for disaster recovery
- Test restore procedures in staging environment

---

## Performance Considerations

### Query Optimization
- All queries use indexed columns (user_id, email)
- Composite index supports sorted queries without separate sort
- Foreign key constraints enable efficient joins

### Connection Pooling
- SQLModel/SQLAlchemy handles connection pooling
- Neon autoscaling handles concurrent connections
- Configure pool size: `pool_size=5, max_overflow=10`

### Scalability
- Neon Serverless scales automatically
- Indexes support efficient queries at scale
- No manual sharding or partitioning required for MVP

---

## Testing Strategy

### Unit Tests
- Test model validation (email format, title length)
- Test default values (completed=false, timestamps)
- Test relationships (user has many tasks)

### Integration Tests
- Test foreign key constraints (cascade delete)
- Test unique constraints (duplicate email)
- Test index performance (query execution time)

### Data Isolation Tests
- Verify user A cannot access user B's tasks
- Verify queries always filter by user_id
- Verify authorization checks on update/delete

---

## Summary

**Tables**: 2 (users, tasks)
**Relationships**: 1:N (one user has many tasks)
**Indexes**: 4 (users.email, tasks.user_id, tasks.(user_id, created_at), users.id)
**Constraints**: 2 foreign keys, 1 unique constraint
**Security**: User data isolation via user_id filtering on all queries

**Ready for**: Implementation via SQLModel ORM in FastAPI backend
