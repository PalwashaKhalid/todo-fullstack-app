# Implementation Plan: Backend API & Data Layer

**Branch**: `002-backend-api-data` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-backend-api-data/spec.md`

## Summary

This plan implements a secure RESTful API backend for task management with strict per-user data isolation. The backend provides CRUD operations for tasks, enforces JWT-based authentication on all endpoints, and persists data to Neon Serverless PostgreSQL. Key technical approach: FastAPI service with JWT verification middleware, SQLModel ORM for type-safe database operations, and authorization checks that filter all queries by authenticated user ID extracted from JWT tokens.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (latest), SQLModel (latest), python-jose[cryptography] (JWT), passlib[bcrypt] (password hashing), uvicorn (ASGI server)
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, auto-scaling)
**Testing**: pytest with FastAPI TestClient, pytest-asyncio for async tests
**Target Platform**: Linux server (containerizable, cloud-deployable)
**Project Type**: Web backend (part of full-stack application)
**Performance Goals**: <500ms response time for single task operations, <1s for task list retrieval (up to 100 tasks), support 100 concurrent users
**Constraints**: JWT validation required on every request, all queries must filter by user_id, no cross-user data access, zero data loss on restart
**Scale/Scope**: Support 10,000 tasks per user, 100+ concurrent users, production-grade error handling and security

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development ✅ PASS
- Feature originates from approved specification (spec.md)
- Following spec → plan → tasks → implement cycle
- All behavior documented in spec.md
- No manual coding - implementation via Claude Code agents

### Principle II: Security-First Architecture ✅ PASS
- JWT authentication enforced on all task endpoints (FR-006, FR-007)
- User data isolation mandatory (FR-008, FR-009)
- JWT verification stateless and deterministic (FR-016)
- User ID extracted from JWT, never from request body (FR-011)
- Database operations scoped to authenticated user (FR-008)
- 401 for missing/invalid JWT, 403 for unauthorized access (FR-007, FR-009)
- Environment variables for secrets (Assumption #2, #3)

### Principle III: Deterministic Implementation ✅ PASS
- API behavior matches spec exactly (all 20 functional requirements)
- Predictable responses with documented JSON schema (FR-014)
- Explicit error handling with documented status codes (FR-013)
- Database schema version-controlled via SQLModel models
- Environment-specific config isolated to .env files

### Principle IV: Clear Separation of Concerns ✅ PASS
- Backend handles only business logic and data access
- Authentication handled by separate Better Auth service (Dependency: Authentication Service)
- Frontend presentation layer separate (out of scope)
- Communication via REST API contracts
- Database access only through SQLModel ORM (FR-017)

### Principle V: Production Realism ✅ PASS
- Real database: Neon Serverless PostgreSQL (Dependency: Relational Data Store)
- Real authentication: JWT tokens from Better Auth (Dependency: Authentication Service)
- Real API contracts: OpenAPI/Swagger documentation
- Real error handling: Comprehensive exception handling (FR-015)
- Real connection management: SQLModel connection pooling

**GATE RESULT**: ✅ ALL PRINCIPLES SATISFIED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/002-backend-api-data/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - JWT verification, SQLModel patterns
├── data-model.md        # Phase 1 output - User and Task entity schemas
├── quickstart.md        # Phase 1 output - Setup and run instructions
├── contracts/           # Phase 1 output - OpenAPI specifications
│   └── openapi.yaml     # REST API contract definitions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Settings management (environment variables)
│   ├── database.py          # Database connection and session management
│   ├── models/              # SQLModel entity definitions
│   │   ├── __init__.py
│   │   ├── user.py          # User model (from auth service)
│   │   └── task.py          # Task model with user_id foreign key
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py          # TaskCreate, TaskUpdate, TaskResponse
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints (if needed)
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── auth/                # Authentication and authorization
│   │   ├── __init__.py
│   │   ├── jwt.py           # JWT verification utilities
│   │   └── dependencies.py  # get_current_user dependency
│   └── middleware/          # Request/response middleware
│       ├── __init__.py
│       └── cors.py          # CORS configuration
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures (test client, test DB)
│   ├── test_auth.py         # JWT verification tests
│   ├── test_tasks.py        # Task CRUD endpoint tests
│   └── test_security.py     # Authorization and isolation tests
├── .env.example             # Environment variable template
├── .env                     # Actual environment variables (gitignored)
├── requirements.txt         # Python dependencies
└── README.md                # Backend setup instructions
```

**Structure Decision**: Web application backend structure selected. The backend/ directory contains the FastAPI application with clear separation between models (data), routers (endpoints), auth (security), and tests. This structure supports the constitution's separation of concerns principle and enables independent testing of each layer.

## Complexity Tracking

> **No violations - this section is empty**

All constitution principles are satisfied without exceptions. The implementation follows standard FastAPI patterns with SQLModel ORM, which aligns perfectly with the constitution's requirements for security-first architecture, deterministic implementation, and production realism.

---

## Phase 0: Research & Technical Decisions

### Research Tasks

1. **JWT Verification with python-jose**
   - Research: How to verify JWT tokens issued by Better Auth in FastAPI
   - Key questions: Token structure, signature verification, expiration handling
   - Output: JWT verification utility function and dependency injection pattern

2. **SQLModel Best Practices**
   - Research: SQLModel patterns for FastAPI integration
   - Key questions: Session management, relationship handling, query filtering
   - Output: Database connection setup and session dependency

3. **FastAPI Security Dependencies**
   - Research: FastAPI dependency injection for authentication
   - Key questions: HTTPBearer security scheme, get_current_user pattern
   - Output: Reusable authentication dependency for all protected routes

4. **Neon PostgreSQL Connection**
   - Research: Connection string format and pooling for Neon Serverless
   - Key questions: SSL requirements, connection pooling settings, timeout handling
   - Output: Database engine configuration with proper pooling

5. **Error Handling Patterns**
   - Research: FastAPI exception handling and custom error responses
   - Key questions: HTTPException usage, global exception handlers, error response format
   - Output: Consistent error response structure matching FR-014

### Technical Decisions to Document

#### Decision 1: Database Schema Design

**Task Fields and Data Types:**
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)  # Owner reference
    title: str = Field(max_length=200)                       # Required, max 200 chars
    description: Optional[str] = Field(default=None, max_length=2000)  # Optional, max 2000 chars
    completed: bool = Field(default=False)                   # Completion status
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**User Ownership Representation:**
- Foreign key constraint: `user_id` references `user.id`
- Index on `user_id` for fast filtering (all queries filter by this)
- Cascade delete: When user deleted, their tasks are deleted (or set to ON DELETE CASCADE)

**Indexing Strategy:**
- Primary index: `id` (auto-created)
- Foreign key index: `user_id` (explicit, for filtering)
- Composite index: `(user_id, created_at)` for sorted task lists
- Rationale: Most queries filter by user_id and sort by created_at (FR-020)

#### Decision 2: Authorization Strategy

**JWT user_id Extraction:**
```python
def get_current_user(token: str = Depends(HTTPBearer())) -> dict:
    try:
        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")  # Standard JWT claim for user ID
        email = payload.get("email")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"id": user_id, "email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**URL user_id Mismatch Handling:**
- Task endpoints don't include user_id in URL (e.g., `/api/tasks/{task_id}`)
- User ID comes only from JWT token via `get_current_user` dependency
- Authorization check: Query filters by both task_id AND user_id from token
- If task not found or belongs to different user: Return 404 (don't reveal existence)
- Alternative: Return 403 if task exists but user doesn't own it (more explicit)

**Decision**: Return 403 for ownership violations to distinguish from genuine 404s

#### Decision 3: API Design Choices

**REST Endpoint Structure:**
```
POST   /api/tasks              # Create task (FR-001)
GET    /api/tasks              # List user's tasks (FR-002)
GET    /api/tasks/{task_id}    # Get specific task (FR-003)
PUT    /api/tasks/{task_id}    # Update task (FR-004)
PATCH  /api/tasks/{task_id}/status  # Toggle completion (FR-004)
DELETE /api/tasks/{task_id}    # Delete task (FR-005)
```

**Request/Response Payload Formats:**

Create Task Request:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

Task Response:
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": 456,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-06T10:30:00Z",
    "updated_at": "2026-02-06T10:30:00Z"
  },
  "message": "Task created successfully"
}
```

List Tasks Response:
```json
{
  "success": true,
  "data": [
    { /* task object */ },
    { /* task object */ }
  ]
}
```

Error Response:
```json
{
  "detail": "Task not found"
}
```

**HTTP Status Code Usage:**
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE
- 400 Bad Request: Validation errors (empty title, too long)
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: Valid JWT but user doesn't own resource
- 404 Not Found: Task doesn't exist
- 500 Internal Server Error: Database errors, unexpected exceptions

#### Decision 4: ORM Usage

**SQLModel Session Management:**
```python
# database.py
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Log SQL in development
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True  # Verify connections before use
)

def get_db():
    with Session(engine) as session:
        yield session
```

**Relationship Handling:**
- No explicit SQLModel relationships defined (keep simple)
- User-Task relationship implicit via foreign key
- Queries use explicit filtering: `select(Task).where(Task.user_id == user_id)`
- Rationale: Simpler than ORM relationships, explicit filtering ensures security

**Query Pattern:**
```python
@router.get("/api/tasks")
async def list_tasks(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    statement = select(Task).where(
        Task.user_id == current_user["id"]
    ).order_by(Task.created_at.desc())
    tasks = db.exec(statement).all()
    return {"success": True, "data": tasks}
```

---

## Phase 1: Design Artifacts

### Artifact 1: data-model.md

**Purpose**: Define SQLModel entity schemas for User and Task

**Content**:
- User model (minimal, from auth service)
- Task model with all fields, constraints, and indexes
- Validation rules (title required, length limits)
- Relationships and foreign keys
- Timestamp handling (auto-set created_at, auto-update updated_at)

### Artifact 2: contracts/openapi.yaml

**Purpose**: OpenAPI 3.0 specification for all API endpoints

**Content**:
- Endpoint definitions (paths, methods, parameters)
- Request body schemas (TaskCreate, TaskUpdate)
- Response schemas (TaskResponse, ErrorResponse)
- Security schemes (Bearer JWT)
- Status code documentation
- Example requests and responses

### Artifact 3: quickstart.md

**Purpose**: Setup and run instructions for backend

**Content**:
- Prerequisites (Python 3.11+, Neon database)
- Environment variable setup (.env configuration)
- Dependency installation (pip install -r requirements.txt)
- Database initialization (create tables)
- Running the server (uvicorn command)
- Testing endpoints (curl examples)
- Troubleshooting common issues

---

## Testing Strategy

### API-Level Validation

**CRUD Operations:**
```python
def test_create_task(client, auth_headers):
    response = client.post(
        "/api/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["data"]["title"] == "Test task"

def test_list_tasks(client, auth_headers):
    # Create 3 tasks
    # List tasks
    # Assert exactly 3 tasks returned

def test_update_task(client, auth_headers):
    # Create task
    # Update title
    # Assert title changed

def test_delete_task(client, auth_headers):
    # Create task
    # Delete task
    # Assert task no longer in list
```

**Task Completion Toggle:**
```python
def test_toggle_completion(client, auth_headers):
    # Create task (completed=False)
    # PATCH /api/tasks/{id}/status with completed=True
    # Assert task.completed == True
    # PATCH again with completed=False
    # Assert task.completed == False
```

### Security Validation

**Authentication Tests:**
```python
def test_no_jwt_returns_401(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401

def test_invalid_jwt_returns_401(client):
    response = client.get(
        "/api/tasks",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

def test_expired_jwt_returns_401(client, expired_token):
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
```

### Data Isolation Tests

**Cross-User Access Prevention:**
```python
def test_user_cannot_read_other_user_tasks(client, user_a_token, user_b_token):
    # User A creates task
    task_response = client.post(
        "/api/tasks",
        json={"title": "User A task"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    task_id = task_response.json()["data"]["id"]

    # User B attempts to read User A's task
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    assert response.status_code == 403  # Forbidden

def test_user_cannot_update_other_user_tasks(client, user_a_token, user_b_token):
    # Similar pattern for update

def test_user_cannot_delete_other_user_tasks(client, user_a_token, user_b_token):
    # Similar pattern for delete

def test_list_tasks_returns_only_own_tasks(client, user_a_token, user_b_token):
    # User A creates 2 tasks
    # User B creates 3 tasks
    # User A lists tasks -> assert 2 tasks
    # User B lists tasks -> assert 3 tasks
```

### Persistence Checks

**Data Survival Tests:**
```python
def test_tasks_persist_after_restart(client, auth_headers):
    # Create task
    # Record task ID
    # Restart application (fixture)
    # Retrieve task by ID
    # Assert task data unchanged

def test_database_constraints_enforced(client, auth_headers):
    # Attempt to create task with empty title
    response = client.post(
        "/api/tasks",
        json={"title": "", "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 400

    # Attempt to create task with title > 200 chars
    response = client.post(
        "/api/tasks",
        json={"title": "x" * 201, "description": "Test"},
        headers=auth_headers
    )
    assert response.status_code == 400
```

---

## Implementation Phases

### Phase 0: Research (Complete via research.md)
- JWT verification patterns with python-jose
- SQLModel session management and query patterns
- FastAPI security dependencies (HTTPBearer, get_current_user)
- Neon PostgreSQL connection configuration
- Error handling and response formatting

### Phase 1: Design (Complete via artifacts)
- data-model.md: User and Task SQLModel schemas
- contracts/openapi.yaml: Complete API specification
- quickstart.md: Setup and run instructions

### Phase 2: Tasks (Next command: /sp.tasks)
- Generate dependency-ordered task list
- Organize by user story (P1, P2, P3)
- Include acceptance criteria per task
- Identify parallel execution opportunities

### Phase 3: Implementation (Next command: /sp.implement)
- Execute tasks via specialized agents
- fastapi-backend agent: API endpoints and business logic
- auth-security-specialist agent: JWT verification and authorization
- neon-db-optimizer agent: Database schema and queries
- Validate against spec at each step

---

## Validation Checklist

### Backend Correctness

- [ ] All 5 task endpoints implemented (POST, GET list, GET single, PUT, DELETE)
- [ ] PATCH endpoint for completion toggle implemented
- [ ] Request validation enforces title required, length limits
- [ ] Response format matches documented schema (success, data, message)
- [ ] HTTP status codes match specification (200, 201, 204, 400, 401, 403, 404, 500)
- [ ] Tasks ordered by created_at DESC by default
- [ ] Filtering by completion status works
- [ ] Timestamps auto-set on creation and update

### Security Validation

- [ ] JWT verification occurs before route execution
- [ ] HTTPBearer security scheme configured
- [ ] get_current_user dependency extracts user ID from JWT
- [ ] All task endpoints require authentication
- [ ] Requests without JWT return 401
- [ ] Requests with invalid JWT return 401
- [ ] Requests with expired JWT return 401
- [ ] User ID from JWT used for all database queries
- [ ] Authorization checks prevent cross-user access
- [ ] Attempts to access other user's tasks return 403
- [ ] Database queries always filter by user_id
- [ ] No user_id accepted from request body or URL

### Data Isolation

- [ ] User A cannot read User B's tasks
- [ ] User A cannot update User B's tasks
- [ ] User A cannot delete User B's tasks
- [ ] List endpoint returns only authenticated user's tasks
- [ ] Task count accurate per user
- [ ] No data leakage in error messages

### Persistence

- [ ] Tasks survive application restart
- [ ] Database connection properly configured
- [ ] SQLModel creates tables on startup
- [ ] Foreign key constraints enforced
- [ ] Indexes created (user_id, composite user_id+created_at)
- [ ] Connection pooling configured
- [ ] Database errors handled gracefully

### API Contract Compliance

- [ ] OpenAPI documentation generated
- [ ] All endpoints documented with examples
- [ ] Request/response schemas match implementation
- [ ] Error responses documented
- [ ] Security scheme documented (Bearer JWT)

---

## Next Steps

1. **Complete Phase 0**: Generate research.md with JWT verification, SQLModel patterns, and error handling research
2. **Complete Phase 1**: Generate data-model.md, contracts/openapi.yaml, and quickstart.md
3. **Update Agent Context**: Run `.specify/scripts/bash/update-agent-context.sh claude` to add FastAPI, SQLModel, and Neon PostgreSQL to agent context
4. **Proceed to /sp.tasks**: Generate actionable task list organized by user story priority
5. **Execute /sp.implement**: Coordinate specialized agents to implement backend

**Plan Status**: ✅ COMPLETE - Ready for Phase 0 research generation
