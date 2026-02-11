# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `001-todo-web-app` | **Date**: 2026-02-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-web-app/spec.md`

## Summary

Transform a console-based Todo application into a secure, multi-user web application with JWT authentication, persistent storage, and full CRUD operations. The system enables users to create accounts, authenticate securely, and manage their personal task lists with complete data isolation between users. Implementation follows the Agentic Dev Stack workflow (spec → plan → tasks → implement) using FastAPI backend, Next.js frontend, Neon PostgreSQL database, and Better Auth with JWT tokens.

## Technical Context

**Language/Version**: Python 3.11+ (Backend), TypeScript/Node.js 18+ (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, uvicorn, python-jose, passlib (Backend); Next.js 16+, Better Auth, React 18+ (Frontend)
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest (Backend), React Testing Library (Frontend), manual verification
**Target Platform**: Web application (Linux/macOS/Windows servers, modern browsers)
**Project Type**: Web application (backend + frontend monorepo)
**Performance Goals**: <50ms p95 API latency, <1.5s First Contentful Paint, 100+ concurrent users
**Constraints**: JWT authentication required, stateless backend, user data isolation mandatory, all code generated via Claude Code
**Scale/Scope**: MVP with 5 user stories (P1-P5), ~78 tasks, 2-layer architecture (frontend + backend)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Principle I: Spec-Driven Development (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: Complete spec.md with 5 user stories, acceptance scenarios, functional requirements (FR-001 to FR-033)
- **Compliance**: All implementation follows spec → plan → tasks → implement workflow via Claude Code

### ✅ Principle II: Security-First Architecture (NON-NEGOTIABLE)
- **Status**: PASS
- **Evidence**: JWT authentication on all protected endpoints, user_id filtering on all queries, Better Auth integration
- **Compliance**: Every API endpoint validates JWT, every database query filters by authenticated user ID, no cross-user data access possible

### ✅ Principle III: Deterministic Implementation
- **Status**: PASS
- **Evidence**: RESTful API contracts defined, OpenAPI documentation, standardized response formats, explicit error handling
- **Compliance**: Same spec produces same behavior, all API responses documented with status codes

### ✅ Principle IV: Clear Separation of Concerns
- **Status**: PASS
- **Evidence**: Authentication layer (Better Auth + JWT), Backend layer (FastAPI + SQLModel), Frontend layer (Next.js App Router), Database layer (Neon PostgreSQL)
- **Compliance**: Each layer has distinct responsibilities, communicates via REST API contracts, no business logic in frontend

### ✅ Principle V: Production Realism
- **Status**: PASS
- **Evidence**: Real database (Neon PostgreSQL), real authentication (Better Auth + JWT), real API contracts (OpenAPI), proper error handling
- **Compliance**: No mocks, no shortcuts, production-grade technologies throughout

**GATE RESULT**: ✅ ALL PRINCIPLES SATISFIED - Proceed to implementation

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-web-app/
├── spec.md              # Feature specification (COMPLETE)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (COMPLETE)
├── data-model.md        # Phase 1 output (database schema design)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   ├── auth-api.yaml   # Authentication endpoints
│   └── tasks-api.yaml  # Task management endpoints
└── tasks.md             # Phase 2 output (COMPLETE - 78 tasks)
```

### Source Code (repository root)

```text
Phase-II/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point, CORS config
│   │   ├── config.py       # Settings management (Pydantic BaseSettings)
│   │   ├── database.py     # Database connection, session management
│   │   ├── models/         # SQLModel schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py     # User model (id, email, hashed_password, created_at)
│   │   │   └── task.py     # Task model (id, user_id, title, description, completed, created_at, updated_at)
│   │   ├── routers/        # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py     # Authentication endpoints (signup, signin, signout)
│   │   │   └── tasks.py    # Task CRUD endpoints
│   │   └── auth/           # JWT validation middleware
│   │       ├── __init__.py
│   │       ├── password.py # Password hashing (bcrypt via passlib)
│   │       ├── jwt.py      # JWT creation and validation (python-jose)
│   │       └── dependencies.py # get_current_user dependency
│   ├── tests/              # Pytest tests
│   │   ├── __init__.py
│   │   ├── test_auth.py    # Authentication tests
│   │   └── test_tasks.py   # Task CRUD tests
│   ├── .env                # Backend environment variables (NOT committed)
│   ├── .env.example        # Environment variable template
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Next.js 16+ App Router
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Landing page
│   │   ├── (auth)/         # Auth-related pages (route group)
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── signup/
│   │   │       └── page.tsx
│   │   └── (dashboard)/    # Protected dashboard pages (route group)
│   │       ├── layout.tsx  # Dashboard layout with signout
│   │       └── page.tsx    # Task dashboard
│   ├── components/         # React components
│   │   ├── TaskList.tsx    # Task list display
│   │   ├── CreateTaskForm.tsx # Task creation form
│   │   ├── EditTaskModal.tsx  # Task edit modal
│   │   └── ui/             # Reusable UI components
│   ├── lib/                # Utilities and helpers
│   │   ├── auth.ts         # Better Auth configuration
│   │   ├── auth-context.tsx # Auth context provider
│   │   └── api-client.ts   # API client with JWT injection
│   ├── middleware.ts       # Protected route middleware
│   ├── .env.local          # Frontend environment variables (NOT committed)
│   ├── .env.example        # Environment variable template
│   ├── package.json        # Node dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   └── next.config.js      # Next.js configuration
│
├── specs/                  # Feature specifications
├── history/                # PHRs and ADRs
├── .specify/               # SpecKit Plus configuration
├── .gitignore              # Git ignore patterns
└── README.md               # Project documentation
```

**Structure Decision**: Web application monorepo structure selected because the project has distinct frontend and backend components that need to communicate via REST API. This structure enables clear separation of concerns (Principle IV), independent scaling, and atomic commits across both layers. The backend/ directory contains the FastAPI application with SQLModel ORM, while frontend/ contains the Next.js App Router application with Better Auth integration.

## Complexity Tracking

> **No violations detected** - All constitution principles are satisfied without exceptions.

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Next.js 16+ Frontend (Port 3000)              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐ │ │
│  │  │ Auth Pages   │  │  Dashboard   │  │  Components     │ │ │
│  │  │ - Signup     │  │  - Task List │  │  - TaskList     │ │ │
│  │  │ - Login      │  │  - Create    │  │  - CreateForm   │ │ │
│  │  └──────────────┘  └──────────────┘  └─────────────────┘ │ │
│  │         │                  │                    │          │ │
│  │         └──────────────────┴────────────────────┘          │ │
│  │                            │                                │ │
│  │                   ┌────────▼────────┐                      │ │
│  │                   │  Better Auth    │                      │ │
│  │                   │  (JWT Tokens)   │                      │ │
│  │                   └────────┬────────┘                      │ │
│  │                            │                                │ │
│  │                   ┌────────▼────────┐                      │ │
│  │                   │  API Client     │                      │ │
│  │                   │  (JWT Injection)│                      │ │
│  │                   └────────┬────────┘                      │ │
│  └────────────────────────────┼─────────────────────────────┘ │
└────────────────────────────────┼───────────────────────────────┘
                                 │
                    HTTP/REST API │ Authorization: Bearer <JWT>
                                 │
┌────────────────────────────────▼───────────────────────────────┐
│              FastAPI Backend (Port 8000)                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                    CORS Middleware                        │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │              JWT Validation Middleware                    │ │
│  │              (get_current_user dependency)                │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │                    API Routers                            │ │
│  │  ┌────────────────┐         ┌────────────────────────┐   │ │
│  │  │  Auth Router   │         │    Tasks Router        │   │ │
│  │  │  - POST signup │         │  - GET /api/tasks      │   │ │
│  │  │  - POST signin │         │  - POST /api/tasks     │   │ │
│  │  │  - POST signout│         │  - PUT /api/tasks/{id} │   │ │
│  │  └────────────────┘         │  - DELETE /api/tasks/{id}│ │
│  │                             │  - PATCH /api/tasks/{id}│  │ │
│  │                             └────────────────────────┘   │ │
│  └──────────────────────────┬───────────────────────────────┘ │
│                             │                                  │
│  ┌──────────────────────────▼───────────────────────────────┐ │
│  │                  SQLModel ORM Layer                       │ │
│  │  ┌────────────────┐         ┌────────────────────────┐   │ │
│  │  │  User Model    │         │    Task Model          │   │ │
│  │  │  - id          │         │  - id                  │   │ │
│  │  │  - email       │         │  - user_id (FK)        │   │ │
│  │  │  - password    │         │  - title               │   │ │
│  │  │  - created_at  │         │  - description         │   │ │
│  │  └────────────────┘         │  - completed           │   │ │
│  │                             │  - created_at          │   │ │
│  │                             │  - updated_at          │   │ │
│  │                             └────────────────────────┘   │ │
│  └──────────────────────────┬───────────────────────────────┘ │
└────────────────────────────────┼───────────────────────────────┘
                                 │
                    SQL Queries  │ (Filtered by user_id)
                                 │
┌────────────────────────────────▼───────────────────────────────┐
│           Neon Serverless PostgreSQL Database                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                      Tables                               │ │
│  │  ┌────────────────┐         ┌────────────────────────┐   │ │
│  │  │  users         │         │    tasks               │   │ │
│  │  │  PK: id        │◄────────│  PK: id                │   │ │
│  │  │  UK: email     │         │  FK: user_id           │   │ │
│  │  │  hashed_pwd    │         │  title (indexed)       │   │ │
│  │  │  created_at    │         │  description           │   │ │
│  │  └────────────────┘         │  completed             │   │ │
│  │                             │  created_at (indexed)  │   │ │
│  │                             │  updated_at            │   │ │
│  │                             └────────────────────────┘   │ │
│  │                                                           │ │
│  │  Indexes:                                                 │ │
│  │  - users.email (UNIQUE)                                   │ │
│  │  - tasks.user_id (for filtering)                          │ │
│  │  - tasks.(user_id, created_at) (for sorted queries)       │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
1. User Signup/Signin
   ┌──────────┐                ┌──────────┐                ┌──────────┐
   │ Frontend │                │ Backend  │                │ Database │
   └────┬─────┘                └────┬─────┘                └────┬─────┘
        │                           │                           │
        │ POST /api/auth/signup     │                           │
        │ {email, password}         │                           │
        ├──────────────────────────►│                           │
        │                           │ Hash password (bcrypt)    │
        │                           │                           │
        │                           │ INSERT INTO users         │
        │                           ├──────────────────────────►│
        │                           │                           │
        │                           │◄──────────────────────────┤
        │                           │ User created              │
        │                           │                           │
        │                           │ Generate JWT token        │
        │                           │ (sign with secret)        │
        │                           │                           │
        │◄──────────────────────────┤                           │
        │ 201 Created               │                           │
        │ {token, user}             │                           │
        │                           │                           │
        │ Store token in session    │                           │
        │                           │                           │

2. Authenticated API Request
   ┌──────────┐                ┌──────────┐                ┌──────────┐
   │ Frontend │                │ Backend  │                │ Database │
   └────┬─────┘                └────┬─────┘                └────┬─────┘
        │                           │                           │
        │ GET /api/tasks            │                           │
        │ Authorization: Bearer JWT │                           │
        ├──────────────────────────►│                           │
        │                           │ Extract JWT from header   │
        │                           │                           │
        │                           │ Verify JWT signature      │
        │                           │ (using shared secret)     │
        │                           │                           │
        │                           │ Decode JWT payload        │
        │                           │ Extract user_id           │
        │                           │                           │
        │                           │ SELECT * FROM tasks       │
        │                           │ WHERE user_id = ?         │
        │                           ├──────────────────────────►│
        │                           │                           │
        │                           │◄──────────────────────────┤
        │                           │ User's tasks only         │
        │                           │                           │
        │◄──────────────────────────┤                           │
        │ 200 OK                    │                           │
        │ {success: true, data: []} │                           │
        │                           │                           │
```

## Implementation Phases

### Phase 0: Research & Architecture (COMPLETE)
- **Status**: ✅ COMPLETE
- **Artifacts**: research.md
- **Key Decisions**: JWT authentication, monorepo structure, RESTful API, user data isolation via database filtering

### Phase 1: Design Artifacts (IN PROGRESS)
- **Status**: 🔄 IN PROGRESS
- **Artifacts**:
  - data-model.md (database schema design)
  - contracts/auth-api.yaml (authentication API contract)
  - contracts/tasks-api.yaml (task management API contract)
  - quickstart.md (setup and run instructions)

### Phase 2: Task Breakdown (COMPLETE)
- **Status**: ✅ COMPLETE
- **Artifacts**: tasks.md (78 tasks organized by user story)

### Phase 3: Implementation (PENDING)
- **Status**: ⏳ PENDING
- **Command**: `/sp.implement`
- **Agents**: auth-security-specialist, fastapi-backend, nextjs-ui-architect, neon-db-optimizer

## Quality Validation Criteria

### Module: Authentication (User Story 1)
- ✅ Users can create accounts with email and password
- ✅ Passwords are hashed with bcrypt (never stored plaintext)
- ✅ Users can sign in and receive JWT token
- ✅ JWT tokens are validated on every protected endpoint
- ✅ Invalid/expired tokens return 401 Unauthorized
- ✅ Unauthenticated users are redirected to login page
- ✅ Users can sign out and session is terminated

### Module: API & Data Layer (User Stories 2-5)
- ✅ All API endpoints follow REST conventions
- ✅ All endpoints return standardized response format
- ✅ All endpoints return appropriate HTTP status codes
- ✅ All database queries filter by authenticated user_id
- ✅ Users cannot access other users' tasks (403 Forbidden)
- ✅ Task CRUD operations work correctly (Create, Read, Update, Delete)
- ✅ Task status can be toggled (complete/incomplete)
- ✅ Data persists across application restarts

### Module: Frontend (User Stories 1-5)
- ✅ Responsive design works on mobile (320px) and desktop (1440px)
- ✅ Forms have proper validation and error messages
- ✅ Loading states displayed during async operations
- ✅ Success feedback shown after operations
- ✅ JWT token automatically attached to API requests
- ✅ Network errors handled gracefully
- ✅ UI updates immediately after successful operations

### Module: Integration (End-to-End)
- ✅ Frontend and backend communicate successfully
- ✅ CORS configured correctly
- ✅ Environment variables loaded properly
- ✅ Database connection established
- ✅ All user stories work independently
- ✅ No cross-user data leakage
- ✅ Application runs without manual intervention

### Module: Security
- ✅ JWT secrets stored in environment variables (never committed)
- ✅ JWT signature validation enforced
- ✅ Token expiration enforced
- ✅ User data isolation enforced on all queries
- ✅ Authorization checks on update/delete operations
- ✅ Input validation on all endpoints
- ✅ SQL injection prevented (parameterized queries)
- ✅ XSS prevented (React auto-escaping + input sanitization)

## Development Approach

### Agentic Dev Stack Workflow

**Current Stage**: Planning (Phase 1 design artifacts)

**Next Steps**:
1. Complete Phase 1 design artifacts (data-model.md, contracts/, quickstart.md)
2. Run `/sp.implement` to execute tasks via specialized agents
3. Agents coordinate implementation:
   - **neon-db-optimizer**: Database schema, indexes, migrations
   - **auth-security-specialist**: Better Auth setup, JWT validation
   - **fastapi-backend**: API endpoints, validation, business logic
   - **nextjs-ui-architect**: Frontend pages, components, responsive design

**Agent Coordination**:
- Phase 2 (Foundational) must complete before any user story work begins
- User stories can then proceed in parallel (if team capacity allows)
- Or sequentially in priority order: P1 → P2 → P3 → P4 → P5
- Each user story is independently testable

### REST API Contract Enforcement

**All endpoints must follow**:
- Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Consistent response format: `{success: bool, data: any, message?: string, errors?: []}`
- Proper status codes (200, 201, 204, 400, 401, 403, 404, 500)
- JWT validation on protected endpoints
- User data isolation on all queries

**Contract validation**:
- OpenAPI specs define exact request/response schemas
- Backend implementation must match specs exactly
- Frontend API client must follow specs exactly
- Any deviation requires spec amendment

### JWT Authentication Verification

**Backend implementation must**:
1. Extract JWT from `Authorization: Bearer <token>` header
2. Verify signature using `BETTER_AUTH_SECRET`
3. Check token expiration
4. Decode payload to extract user_id
5. Use user_id for all database queries
6. Return 401 if token missing/invalid/expired
7. Return 403 if user doesn't own requested resource

**Frontend implementation must**:
1. Store JWT token from Better Auth session
2. Include token in all API requests
3. Handle 401 by redirecting to login
4. Handle 403 by showing error message
5. Handle token expiration gracefully

### Data Persistence via Neon + SQLModel

**Database requirements**:
- Neon Serverless PostgreSQL connection
- SQLModel ORM for type-safe queries
- Connection pooling configured
- All tables have proper indexes
- Foreign key constraints enforced
- Timestamps (created_at, updated_at) on all entities

**Data isolation requirements**:
- Every query MUST filter by user_id
- No query can return data from other users
- Authorization checks on update/delete
- Database indexes on user_id for performance

## Risk Mitigation

### Technical Risks
- **JWT secret leaked**: Store in environment variables, never commit, rotate regularly
- **Database connection exhaustion**: Connection pooling, Neon auto-scaling
- **CORS misconfiguration**: Explicit CORS origins in config, test cross-origin requests
- **Token expiration UX**: Clear error messages, automatic redirect to login

### Security Risks
- **User data leakage**: Every query filtered by user_id, authorization checks on all operations
- **XSS attacks**: Input sanitization, React auto-escaping
- **SQL injection**: Parameterized queries via SQLModel
- **Session hijacking**: HTTPS only in production, short token expiration

### Operational Risks
- **Environment variable misconfiguration**: Validation on startup, clear error messages
- **Deployment failures**: Test in staging, rollback plan
- **Database migration failures**: Test migrations in dev, backup before production

## Success Metrics

**Functional Completeness**:
- All 5 user stories implemented and independently testable
- All 33 functional requirements (FR-001 to FR-033) satisfied
- All acceptance scenarios from spec.md passing

**Security Validation**:
- Multi-user authentication fully functional
- Zero cross-user data leakage
- JWT validation working on all protected endpoints
- All security checklist items passing

**Integration Validation**:
- Frontend, backend, and database work together seamlessly
- API contracts match specification exactly
- Error handling works end-to-end
- Application runs without manual intervention

**Quality Validation**:
- Application is spec-compliant and traceable
- All code generated through Agentic Dev Stack workflow
- PHRs document all development decisions
- Project is review-ready for hackathon judging

## Next Steps

1. **Complete Phase 1 design artifacts** (this planning session):
   - ✅ plan.md (this file)
   - ⏳ data-model.md
   - ⏳ contracts/auth-api.yaml
   - ⏳ contracts/tasks-api.yaml
   - ⏳ quickstart.md

2. **Update agent context**:
   ```bash
   .specify/scripts/bash/update-agent-context.sh claude
   ```

3. **Execute implementation**:
   ```bash
   /sp.implement
   ```

4. **Validate each user story independently** after implementation

5. **Create PHR** to document this planning session

---

**Plan Status**: Phase 1 design artifacts in progress
**Ready for**: Implementation via `/sp.implement` after Phase 1 completion
**Constitution Compliance**: ✅ All 5 principles satisfied
