# Tasks: Backend API & Data Layer

**Feature**: Backend API & Data Layer (002-backend-api-data)
**Branch**: `002-backend-api-data`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Overview

This document breaks down the Backend API & Data Layer implementation into actionable tasks organized by user story priority. Each user story represents an independently testable increment of functionality.

**Technology Stack:**
- Python 3.11+
- FastAPI (latest)
- SQLModel (latest)
- python-jose[cryptography] (JWT verification)
- passlib[bcrypt] (password hashing)
- uvicorn (ASGI server)
- Neon Serverless PostgreSQL

**Implementation Strategy:**
- MVP First: User Story 1 (P1) delivers core create/retrieve functionality
- Incremental Delivery: Each story builds on previous stories
- Independent Testing: Each story can be tested independently
- Security First: JWT authentication enforced from the start

---

## Task Summary

| Phase | User Story | Task Count | Parallelizable |
|-------|-----------|------------|----------------|
| Phase 1: Setup | N/A | 5 | 3 |
| Phase 2: Foundational | N/A | 8 | 5 |
| Phase 3: User Story 1 (P1) | Create and Retrieve Tasks | 6 | 3 |
| Phase 4: User Story 2 (P2) | Update and Delete Tasks | 4 | 3 |
| Phase 5: User Story 3 (P3) | Persistent Storage | 3 | 2 |
| Phase 6: Polish | Cross-Cutting Concerns | 5 | 4 |
| **Total** | | **31** | **20** |

---

## Phase 1: Setup

**Goal**: Initialize project structure and development environment

**Prerequisites**: None

**Completion Criteria**:
- Backend directory structure created per plan.md
- All dependencies installed
- Environment variables configured
- Development server can start

### Tasks

- [ ] T001 Create backend project directory structure per plan.md (backend/app/, backend/tests/, backend/app/models/, backend/app/schemas/, backend/app/routers/, backend/app/auth/, backend/app/middleware/)
- [ ] T002 [P] Create requirements.txt with all dependencies (fastapi, sqlmodel, uvicorn, python-jose, passlib, psycopg2-binary, pydantic-settings, pytest, httpx)
- [ ] T003 [P] Create .env.example file with template environment variables (DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, BETTER_AUTH_SECRET, API_HOST, API_PORT, CORS_ORIGINS)
- [ ] T004 [P] Create .gitignore file to exclude .env, venv/, __pycache__/, *.pyc, .pytest_cache/
- [ ] T005 Install dependencies in virtual environment (python -m venv venv && source venv/bin/activate && pip install -r requirements.txt)

---

## Phase 2: Foundational

**Goal**: Implement core infrastructure required by all user stories

**Prerequisites**: Phase 1 complete

**Completion Criteria**:
- Database connection established
- JWT verification working
- User model created
- FastAPI app initialized
- Authentication dependency available

### Tasks

- [ ] T006 [P] Implement configuration management in backend/app/config.py (Settings class with pydantic-settings, load from .env, DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, BETTER_AUTH_SECRET, CORS_ORIGINS)
- [ ] T007 [P] Implement database connection in backend/app/database.py (create_engine with Neon SSL, connection pooling: pool_size=5, max_overflow=10, pool_pre_ping=True, get_db dependency function)
- [ ] T008 [P] Create User model in backend/app/models/user.py (SQLModel with id, email, hashed_password, created_at fields, __tablename__="users")
- [ ] T009 [P] Implement JWT verification utilities in backend/app/auth/jwt.py (verify_jwt_token function using python-jose, handle ExpiredSignatureError and JWTError, return payload dict)
- [ ] T010 [P] Implement get_current_user dependency in backend/app/auth/dependencies.py (HTTPBearer security, extract token, verify with jwt.py, return user dict with id and email)
- [ ] T011 Initialize FastAPI application in backend/app/main.py (create FastAPI app, configure CORS middleware with settings.cors_origins_list, add health check endpoint GET /, GET /health)
- [ ] T012 Create database initialization function in backend/app/database.py (create_db_and_tables using SQLModel.metadata.create_all, call on app startup event)
- [ ] T013 Create __init__.py files in all backend/app/ subdirectories (models/, schemas/, routers/, auth/, middleware/)

---

## Phase 3: User Story 1 - Create and Retrieve Personal Tasks (P1)

**User Story**: As an authenticated user, I want to create tasks and retrieve only my own tasks so that I can manage my personal to-do list without seeing other users' data.

**Goal**: Implement MVP functionality - task creation and retrieval with user isolation

**Prerequisites**: Phase 2 complete

**Independent Test Criteria**:
- ✅ Authenticated user can create a task with title and description
- ✅ Created task is stored with user_id from JWT token
- ✅ User can retrieve list of their own tasks
- ✅ User can retrieve a specific task by ID
- ✅ User only sees their own tasks (no cross-user data)
- ✅ Unauthenticated requests return 401
- ✅ Tasks ordered by created_at DESC

**Acceptance Scenarios**:
1. Given a user is authenticated with valid token, When they create a task, Then task is stored with their user_id and unique ID returned
2. Given a user has created 3 tasks, When they request task list, Then they receive exactly those 3 tasks
3. Given two users (Alice and Bob) each create tasks, When Alice requests her list, Then she sees only her tasks
4. Given a user is not authenticated, When they attempt to create/retrieve tasks, Then request is rejected with 401

### Tasks

- [ ] T014 [P] [US1] Create Task model in backend/app/models/task.py (SQLModel with id, user_id foreign key, title, description, completed, created_at, updated_at, __tablename__="tasks", indexes on user_id and (user_id, created_at))
- [ ] T015 [P] [US1] Create Task request/response schemas in backend/app/schemas/task.py (TaskCreate with title and description, TaskResponse with all fields, TaskListResponse)
- [ ] T016 [US1] Create tasks router in backend/app/routers/tasks.py (APIRouter with prefix="/api/tasks", tag="tasks")
- [ ] T017 [US1] Implement POST /api/tasks endpoint in backend/app/routers/tasks.py (create_task function, require get_current_user dependency, validate title not empty, associate task with current_user["id"], return 201 with TaskResponse)
- [ ] T018 [US1] Implement GET /api/tasks endpoint in backend/app/routers/tasks.py (list_tasks function, require get_current_user dependency, filter by user_id, order by created_at DESC, support optional completed query param, return TaskListResponse)
- [ ] T019 [US1] Implement GET /api/tasks/{task_id} endpoint in backend/app/routers/tasks.py (get_task function, require get_current_user dependency, filter by task_id AND user_id, return 404 if not found, return 403 if belongs to different user, return TaskResponse)
- [ ] T020 Register tasks router in backend/app/main.py (app.include_router(tasks.router))

---

## Phase 4: User Story 2 - Update and Delete Personal Tasks (P2)

**User Story**: As an authenticated user, I want to update and delete my own tasks so that I can modify my to-do list as my needs change, while being prevented from modifying other users' tasks.

**Goal**: Complete CRUD operations with authorization checks

**Prerequisites**: Phase 3 complete (User Story 1 implemented)

**Independent Test Criteria**:
- ✅ User can update task title and description
- ✅ User can toggle task completion status
- ✅ User can delete their own tasks
- ✅ User cannot update/delete another user's tasks (403)
- ✅ Attempting to modify non-existent task returns 404
- ✅ Updated tasks have updated_at timestamp changed

**Acceptance Scenarios**:
1. Given a user owns a task, When they update title/description, Then changes are persisted
2. Given a user owns a task, When they mark it complete/incomplete, Then status is updated
3. Given a user owns a task, When they delete it, Then task is removed from their list
4. Given a user attempts to update/delete another user's task, Then request is rejected with 403
5. Given a user attempts to update/delete non-existent task, Then request is rejected with 404

### Tasks

- [ ] T021 [P] [US2] Create TaskUpdate schema in backend/app/schemas/task.py (title and description fields, both required)
- [ ] T022 [P] [US2] Create TaskStatusUpdate schema in backend/app/schemas/task.py (completed boolean field)
- [ ] T023 [US2] Implement PUT /api/tasks/{task_id} endpoint in backend/app/routers/tasks.py (update_task function, require get_current_user dependency, filter by task_id AND user_id, validate title not empty, update title and description, set updated_at to current time, return 404 if not found, return 403 if different user, return TaskResponse)
- [ ] T024 [P] [US2] Implement PATCH /api/tasks/{task_id}/status endpoint in backend/app/routers/tasks.py (update_task_status function, require get_current_user dependency, filter by task_id AND user_id, update completed field, set updated_at to current time, return 404 if not found, return 403 if different user, return TaskResponse)
- [ ] T025 [US2] Implement DELETE /api/tasks/{task_id} endpoint in backend/app/routers/tasks.py (delete_task function, require get_current_user dependency, filter by task_id AND user_id, delete task, return 204 No Content, return 404 if not found, return 403 if different user)

---

## Phase 5: User Story 3 - Persistent Task Storage Across Sessions (P3)

**User Story**: As a user, I want my tasks to persist across application restarts and sessions so that my data is never lost and I can access it from any device.

**Goal**: Ensure data persistence and reliability

**Prerequisites**: Phase 4 complete (User Story 2 implemented)

**Independent Test Criteria**:
- ✅ Tasks survive application restart
- ✅ Task data remains unchanged after restart (including timestamps)
- ✅ Multiple users' tasks persist independently
- ✅ Database connection recovers from temporary failures
- ✅ Foreign key constraints enforced

**Acceptance Scenarios**:
1. Given a user has created tasks, When backend service is restarted, Then all tasks remain accessible
2. Given a user creates a task at time T1, When they retrieve it at time T2 (later), Then task data is identical
3. Given multiple users have tasks, When data store connection is lost and restored, Then all users can still access their tasks

### Tasks

- [ ] T026 [P] [US3] Verify database table creation on startup in backend/app/database.py (ensure create_db_and_tables is called in @app.on_event("startup"), verify tables exist: users, tasks)
- [ ] T027 [P] [US3] Verify foreign key constraints in backend/app/models/task.py (user_id references users.id, ON DELETE CASCADE behavior)
- [ ] T028 [US3] Verify connection pooling configuration in backend/app/database.py (pool_size=5, max_overflow=10, pool_pre_ping=True for connection health checks, pool_recycle=3600 for Neon serverless)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Enhance error handling, validation, and documentation

**Prerequisites**: Phase 5 complete (all user stories implemented)

**Completion Criteria**:
- Comprehensive error handling
- Input validation on all endpoints
- OpenAPI documentation accessible
- CORS properly configured
- Production-ready logging

### Tasks

- [ ] T029 [P] Add global exception handler in backend/app/main.py (@app.exception_handler(Exception), log error details, return 500 with generic message, don't expose internal details)
- [ ] T030 [P] Add request validation error handler in backend/app/main.py (handle Pydantic ValidationError, return 400 with field-specific errors)
- [ ] T031 [P] Add database error handling in backend/app/routers/tasks.py (catch IntegrityError and OperationalError, rollback transaction, return appropriate error responses)
- [ ] T032 [P] Verify OpenAPI documentation generation (access http://localhost:8001/docs, verify all endpoints documented, verify Bearer auth scheme shown, verify request/response schemas match openapi.yaml)
- [ ] T033 Update backend/README.md with setup instructions (prerequisites, installation steps, environment configuration, running the server, testing endpoints, troubleshooting)

---

## Dependencies & Execution Order

### User Story Dependencies

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational)
    ↓
Phase 3 (User Story 1 - P1) ← MVP - Can deploy after this
    ↓
Phase 4 (User Story 2 - P2) ← Complete CRUD
    ↓
Phase 5 (User Story 3 - P3) ← Production-ready
    ↓
Phase 6 (Polish)
```

**Critical Path**: T001 → T005 → T006-T013 → T014-T020 → T021-T025 → T026-T028 → T029-T033

**Blocking Tasks** (must complete before others):
- T001: Project structure (blocks all)
- T002: Dependencies (blocks all)
- T006: Configuration (blocks database and auth)
- T007: Database connection (blocks models)
- T008: User model (blocks Task model)
- T009-T010: JWT auth (blocks all endpoints)
- T011: FastAPI app (blocks all endpoints)
- T014: Task model (blocks all task endpoints)
- T015: Task schemas (blocks all task endpoints)

### Parallel Execution Opportunities

**Phase 1 - Can run in parallel:**
- T002, T003, T004 (file creation tasks)

**Phase 2 - Can run in parallel after T001-T005:**
- T006, T007, T008, T009, T010 (independent infrastructure components)

**Phase 3 - Can run in parallel after T006-T013:**
- T014, T015 (model and schemas are independent)
- After T014-T016 complete: T017, T018, T019 (different endpoints)

**Phase 4 - Can run in parallel after Phase 3:**
- T021, T022 (schema definitions)
- After T021-T022: T024 (PATCH endpoint independent of PUT/DELETE)

**Phase 5 - Can run in parallel after Phase 4:**
- T026, T027 (verification tasks)

**Phase 6 - Can run in parallel after Phase 5:**
- T029, T030, T031, T032 (independent polish tasks)

---

## MVP Scope

**Minimum Viable Product**: Phase 1 + Phase 2 + Phase 3 (User Story 1)

**Delivers**:
- Authenticated task creation
- Task list retrieval with user isolation
- Individual task retrieval
- JWT-based security
- Persistent storage

**MVP Task Count**: 20 tasks (T001-T020)

**Estimated Effort**:
- Setup: 1-2 hours
- Foundational: 3-4 hours
- User Story 1: 2-3 hours
- **Total MVP**: 6-9 hours

---

## Implementation Strategy

### Incremental Delivery

1. **Sprint 1 (MVP)**: Phases 1-3
   - Deliverable: Users can create and view their tasks
   - Value: Core functionality, immediate usability
   - Testing: Create tasks, list tasks, verify user isolation

2. **Sprint 2 (Complete CRUD)**: Phase 4
   - Deliverable: Users can update and delete tasks
   - Value: Full task management capabilities
   - Testing: Update tasks, toggle completion, delete tasks

3. **Sprint 3 (Production-Ready)**: Phases 5-6
   - Deliverable: Persistent storage and polish
   - Value: Reliability and production readiness
   - Testing: Restart server, verify persistence, test error handling

### Testing Approach

**Per User Story Testing** (after each phase):

**User Story 1 (P1) - Create and Retrieve:**
```bash
# Test 1: Create task
curl -X POST http://localhost:8001/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"Test description"}'

# Test 2: List tasks
curl -X GET http://localhost:8001/api/tasks \
  -H "Authorization: Bearer $TOKEN"

# Test 3: Get specific task
curl -X GET http://localhost:8001/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"

# Test 4: Verify user isolation (use different user token)
curl -X GET http://localhost:8001/api/tasks \
  -H "Authorization: Bearer $TOKEN_USER2"
```

**User Story 2 (P2) - Update and Delete:**
```bash
# Test 1: Update task
curl -X PUT http://localhost:8001/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title","description":"Updated description"}'

# Test 2: Toggle completion
curl -X PATCH http://localhost:8001/api/tasks/1/status \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Test 3: Delete task
curl -X DELETE http://localhost:8001/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

**User Story 3 (P3) - Persistence:**
```bash
# Test 1: Create tasks, restart server, verify tasks still exist
# Test 2: Check timestamps unchanged after restart
# Test 3: Verify multiple users' data persists independently
```

---

## Validation Checklist

### Task Format Validation
- [x] All tasks have checkbox format: `- [ ]`
- [x] All tasks have sequential IDs: T001, T002, T003...
- [x] Parallelizable tasks marked with [P]
- [x] User story tasks have [US#] labels
- [x] All tasks have clear descriptions
- [x] All tasks specify file paths

### Completeness Validation
- [x] All user stories from spec.md covered
- [x] All entities from data-model.md included
- [x] All endpoints from openapi.yaml included
- [x] All technical decisions from plan.md addressed
- [x] Setup and foundational tasks included
- [x] Polish and cross-cutting concerns included

### Organization Validation
- [x] Tasks organized by user story priority
- [x] Each user story has independent test criteria
- [x] Dependencies clearly documented
- [x] Parallel execution opportunities identified
- [x] MVP scope clearly defined

---

## Notes

**Security Reminders**:
- All task endpoints MUST use get_current_user dependency
- All database queries MUST filter by user_id from JWT token
- Never trust user_id from request body or URL parameters
- Return 401 for missing/invalid JWT, 403 for authorization failures

**Database Reminders**:
- Use SQLModel for all database operations (no raw SQL)
- Always use parameterized queries (SQLModel handles this)
- Set pool_pre_ping=True for Neon serverless reliability
- Use UTC for all timestamps

**Testing Reminders**:
- Test each user story independently after implementation
- Verify user isolation (cross-user access prevention)
- Test with multiple users to ensure data isolation
- Verify persistence by restarting server

---

**Status**: ✅ Tasks ready for implementation via `/sp.implement`
