# Research: Backend API & Data Layer

**Feature**: Backend API & Data Layer (002-backend-api-data)
**Date**: 2026-02-06
**Purpose**: Document technical research findings for JWT verification, SQLModel patterns, FastAPI security, Neon PostgreSQL connection, and error handling

---

## 1. JWT Verification with python-jose

### Research Question
How to verify JWT tokens issued by Better Auth in FastAPI backend?

### Findings

**Token Structure:**
- Better Auth issues standard JWT tokens with claims: `sub` (user ID), `email`, `exp` (expiration), `iat` (issued at)
- Tokens are signed using HS256 algorithm with shared secret (BETTER_AUTH_SECRET)
- Format: `Authorization: Bearer <token>` header

**Signature Verification:**
```python
from jose import jwt, JWTError
from fastapi import HTTPException

def verify_jwt_token(token: str, secret: str, algorithm: str = "HS256") -> dict:
    """
    Verify JWT token signature and extract payload.

    Args:
        token: JWT token string
        secret: Shared secret key for verification
        algorithm: JWT algorithm (default: HS256)

    Returns:
        Decoded payload dictionary

    Raises:
        HTTPException: 401 if token invalid or expired
    """
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Expiration Handling:**
- python-jose automatically validates `exp` claim during decode
- Expired tokens raise `ExpiredSignatureError`
- Frontend should handle 401 responses by refreshing token or redirecting to login

**Dependency Injection Pattern:**
```python
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Extract and verify JWT token from Authorization header.
    Returns user information from token payload.
    """
    token = credentials.credentials
    payload = verify_jwt_token(token, settings.JWT_SECRET_KEY)

    user_id = payload.get("sub")
    email = payload.get("email")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return {"id": user_id, "email": email}
```

**Decision**: Use python-jose for JWT verification with HTTPBearer security scheme and dependency injection for authentication.

---

## 2. SQLModel Best Practices

### Research Question
What are the recommended patterns for SQLModel integration with FastAPI?

### Findings

**Session Management:**
```python
from sqlmodel import create_engine, Session

# Create engine with connection pooling
engine = create_engine(
    database_url,
    echo=True,  # Log SQL queries in development
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Additional connections when pool exhausted
    pool_pre_ping=True,  # Verify connection health before use
    pool_recycle=3600  # Recycle connections after 1 hour
)

# Dependency for database sessions
def get_db():
    """
    Provide database session for request.
    Session automatically closed after request completes.
    """
    with Session(engine) as session:
        yield session
```

**Relationship Handling:**
- **Simple approach**: Use foreign keys without explicit relationships
- **Benefit**: Explicit queries, clear security filtering, no lazy loading issues
- **Pattern**: Always filter by user_id in queries

```python
# Query pattern with explicit filtering
statement = select(Task).where(
    Task.user_id == current_user["id"]
).order_by(Task.created_at.desc())
tasks = db.exec(statement).all()
```

**Query Filtering Best Practices:**
- Always include user_id filter for user-owned resources
- Use parameterized queries (SQLModel handles this automatically)
- Avoid raw SQL to prevent injection attacks
- Use `select()` for type-safe queries

**Model Definition:**
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Decision**: Use simple foreign keys without explicit relationships, always filter queries by user_id, leverage SQLModel's type safety.

---

## 3. FastAPI Security Dependencies

### Research Question
How to implement FastAPI dependency injection for authentication?

### Findings

**HTTPBearer Security Scheme:**
```python
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Use in route
@router.get("/api/tasks")
async def list_tasks(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    # credentials.credentials contains the token
    pass
```

**get_current_user Pattern:**
```python
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Reusable dependency that:
    1. Extracts JWT from Authorization header
    2. Verifies token signature and expiration
    3. Returns user information

    Raises HTTPException(401) if authentication fails.
    """
    token = credentials.credentials
    payload = verify_jwt_token(token, settings.JWT_SECRET_KEY)
    return {"id": payload.get("sub"), "email": payload.get("email")}

# Use in protected routes
@router.get("/api/tasks")
async def list_tasks(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # current_user contains {"id": ..., "email": ...}
    # Use current_user["id"] to filter queries
    pass
```

**Dependency Composition:**
- Dependencies can depend on other dependencies
- FastAPI resolves dependency tree automatically
- Exceptions in dependencies propagate to route handler

**OpenAPI Integration:**
- HTTPBearer automatically adds security to OpenAPI schema
- Swagger UI shows "Authorize" button for testing with tokens

**Decision**: Use HTTPBearer with get_current_user dependency for all protected routes. This provides automatic OpenAPI documentation and consistent authentication.

---

## 4. Neon PostgreSQL Connection

### Research Question
What are the connection requirements for Neon Serverless PostgreSQL?

### Findings

**Connection String Format:**
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

**SSL Requirements:**
- Neon requires SSL connections (`sslmode=require`)
- Connection string must include `?sslmode=require` parameter
- No additional SSL certificate configuration needed

**Connection Pooling Settings:**
```python
engine = create_engine(
    database_url,
    pool_size=5,  # Neon recommends 5-10 for serverless
    max_overflow=10,  # Allow burst traffic
    pool_pre_ping=True,  # Critical for serverless - verify connection health
    pool_recycle=3600,  # Recycle after 1 hour (Neon may close idle connections)
    connect_args={
        "connect_timeout": 10,  # 10 second connection timeout
        "options": "-c timezone=utc"  # Use UTC for timestamps
    }
)
```

**Serverless Considerations:**
- Neon auto-scales and may pause inactive databases
- `pool_pre_ping=True` ensures connections are valid before use
- Keep pool size modest (5-10) for serverless workloads
- Neon handles connection limits automatically

**Timeout Handling:**
- Set reasonable connection timeout (10 seconds)
- Handle connection errors gracefully with try/except
- Return 500 error if database unavailable

**Decision**: Use connection pooling with pool_pre_ping=True, SSL required, modest pool size (5), and proper timeout handling.

---

## 5. Error Handling Patterns

### Research Question
How to implement consistent error handling in FastAPI?

### Findings

**HTTPException Usage:**
```python
from fastapi import HTTPException

# Standard error responses
raise HTTPException(status_code=400, detail="Title cannot be empty")
raise HTTPException(status_code=401, detail="Invalid or expired token")
raise HTTPException(status_code=403, detail="Not authorized to access this task")
raise HTTPException(status_code=404, detail="Task not found")
raise HTTPException(status_code=500, detail="Internal server error")
```

**Global Exception Handlers:**
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch all unhandled exceptions and return consistent error response.
    Log error details for debugging without exposing to client.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

**Error Response Format:**
FastAPI default format:
```json
{
  "detail": "Error message"
}
```

Custom format (if needed):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title cannot be empty",
    "field": "title"
  }
}
```

**Validation Errors:**
- Pydantic automatically validates request bodies
- Returns 422 Unprocessable Entity with detailed field errors
- Can customize with custom exception handler

**Database Error Handling:**
```python
from sqlalchemy.exc import IntegrityError, OperationalError

try:
    db.add(task)
    db.commit()
except IntegrityError as e:
    db.rollback()
    raise HTTPException(status_code=400, detail="Database constraint violation")
except OperationalError as e:
    db.rollback()
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database connection error")
```

**Decision**: Use FastAPI's default HTTPException for standard errors, add global exception handler for unhandled exceptions, handle database errors explicitly with rollback.

---

## Summary of Technical Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| JWT Verification | python-jose with HTTPBearer | Standard library, automatic OpenAPI integration |
| Session Management | SQLModel with connection pooling | Type-safe, automatic session cleanup |
| Authentication | get_current_user dependency | Reusable, consistent, automatic security |
| Database Connection | Neon with SSL, pool_pre_ping | Serverless-optimized, connection health checks |
| Error Handling | HTTPException + global handler | Consistent responses, proper logging |
| Query Pattern | Explicit filtering by user_id | Security-first, no lazy loading issues |
| Relationships | Foreign keys without ORM relationships | Simpler, explicit, secure |

---

## Implementation Readiness

All research tasks completed. Key findings:
- JWT verification pattern established with python-jose
- SQLModel session management and query patterns defined
- FastAPI security dependencies designed (HTTPBearer + get_current_user)
- Neon PostgreSQL connection configuration determined
- Error handling strategy established

**Status**: ✅ Ready for Phase 1 (Design Artifacts)
