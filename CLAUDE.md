# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Project Overview

This project transforms a console application into a modern multi-user web application using the Agentic Dev Stack workflow: **spec → plan → tasks → implement**.

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth (JWT tokens) |
| Development | Claude Code + Spec-Kit Plus |

### Authentication Architecture

**Better Auth with JWT Flow:**
1. User logs in on Frontend → Better Auth creates session and issues JWT token
2. Frontend makes API call → Includes JWT in `Authorization: Bearer <token>` header
3. Backend receives request → Extracts token, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID, email, etc.
5. Backend filters data → Returns only resources belonging to authenticated user

**Security Requirements:**
- Never hardcode JWT secrets; use environment variables
- Validate JWT signature on every protected endpoint
- Match user ID from token with user ID in request URL/body
- Implement proper error handling for expired/invalid tokens

## Agent Delegation Strategy

This project uses specialized agents for different layers of the stack. You MUST delegate work to the appropriate agent based on the task domain.

### When to Use Auth Agent (`auth-security-specialist`)

**Trigger this agent for:**
- Implementing signup/signin flows
- JWT token generation and validation
- Better Auth integration and configuration
- Password hashing and security
- Session management
- Role-based access control (RBAC)
- Security audits of authentication code
- Token lifecycle management (refresh, expiration)

**Example scenarios:**
- "Implement user signup with Better Auth"
- "Add JWT validation middleware to FastAPI"
- "Review authentication security vulnerabilities"
- "Configure Better Auth for Next.js App Router"

### When to Use Frontend Agent (`nextjs-ui-architect`)

**Trigger this agent for:**
- Building Next.js pages and components
- Responsive UI/UX implementation
- Client-side routing (App Router)
- Form handling and validation
- State management
- Performance optimization (Core Web Vitals)
- Accessibility (WCAG compliance)
- CSS/Tailwind styling

**Example scenarios:**
- "Create a responsive dashboard page"
- "Build a task list component with filtering"
- "Optimize page load performance"
- "Fix mobile layout issues"

### When to Use Database Agent (`neon-db-optimizer`)

**Trigger this agent for:**
- Database schema design
- Table creation and migrations
- Index optimization
- Query performance issues
- Neon-specific features (branching, connection pooling)
- Database cost optimization
- Data modeling and normalization
- SQLModel schema definitions

**Example scenarios:**
- "Design database schema for multi-user task management"
- "Optimize slow query on tasks table"
- "Set up Neon database branching for staging"
- "Create migration for adding user_id foreign key"

### When to Use Backend Agent (`fastapi-backend`)

**Trigger this agent for:**
- FastAPI endpoint implementation
- Request/response validation (Pydantic models)
- API route organization
- Database query logic (SQLModel)
- Error handling and HTTP status codes
- API documentation (OpenAPI/Swagger)
- Middleware implementation
- Background tasks and async operations

**Example scenarios:**
- "Create POST /api/tasks endpoint"
- "Add validation for task creation request"
- "Implement user-specific data filtering"
- "Review API error handling patterns"

### Agent Coordination

**Multi-layer features require sequential agent usage:**

1. **Authentication feature:**
   - DB Agent → Design user schema
   - Auth Agent → Implement Better Auth + JWT
   - Backend Agent → Add protected endpoints
   - Frontend Agent → Build login/signup UI

2. **CRUD feature (e.g., tasks):**
   - DB Agent → Design task schema with user_id
   - Backend Agent → Create API endpoints with JWT validation
   - Frontend Agent → Build UI components

3. **Performance optimization:**
   - DB Agent → Optimize queries and indexes
   - Backend Agent → Review API efficiency
   - Frontend Agent → Optimize rendering and loading

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

## Project-Specific Requirements

### No Manual Coding Policy
**CRITICAL:** This project follows the Agentic Dev Stack workflow. All code must be generated through the spec → plan → tasks → implement cycle using Claude Code and Spec-Kit Plus. Manual coding is not allowed.

**Workflow enforcement:**
1. Start with `/sp.specify` to create feature specification
2. Use `/sp.plan` to generate architectural plan
3. Use `/sp.tasks` to break down into actionable tasks
4. Use `/sp.implement` to execute implementation
5. Review and iterate through agents, not manual edits

### RESTful API Standards

**Endpoint naming conventions:**
- Use plural nouns: `/api/tasks`, `/api/users`
- Use HTTP methods correctly: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- Include resource IDs in path: `/api/tasks/{task_id}`

**Response format:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "errors": []
}
```

**Status codes:**
- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (valid token, insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

### Multi-User Data Isolation

**CRITICAL SECURITY REQUIREMENT:** Every database query must filter by authenticated user.

**Pattern for protected endpoints:**
```python
@router.get("/api/tasks")
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ALWAYS filter by user_id from JWT token
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks
```

**Validation checklist:**
- [ ] Extract user ID from JWT token
- [ ] Validate token signature and expiration
- [ ] Filter all queries by `user_id`
- [ ] Prevent users from accessing other users' data
- [ ] Return 403 if user tries to access unauthorized resources

### Database Schema Requirements

**All user-owned tables must include:**
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)  # REQUIRED
    # ... other fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Index strategy:**
- Always index `user_id` for fast filtering
- Add composite indexes for common query patterns: `(user_id, created_at)`
- Use Neon's autoscaling; avoid over-indexing

### Frontend-Backend Integration

**API client pattern (Next.js):**
```typescript
// Use fetch with JWT from Better Auth session
const response = await fetch('/api/tasks', {
  headers: {
    'Authorization': `Bearer ${session.token}`,
    'Content-Type': 'application/json'
  }
});
```

**Error handling:**
- Display user-friendly messages for 400/401/403 errors
- Redirect to login on 401
- Show validation errors inline on forms
- Log 500 errors and show generic message to user

### Environment Configuration

**Required environment variables:**

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql://user:password@host/dbname
NEON_DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Better Auth Integration
BETTER_AUTH_SECRET=shared-secret-with-frontend
BETTER_AUTH_URL=http://localhost:3000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Frontend (.env.local):**
```bash
# Better Auth
BETTER_AUTH_SECRET=shared-secret-with-backend
BETTER_AUTH_URL=http://localhost:3000

# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database (for Better Auth)
DATABASE_URL=postgresql://user:password@host/dbname
```

**Security checklist:**
- [ ] Never commit .env files to git
- [ ] Use different secrets for dev/staging/production
- [ ] Rotate JWT secrets periodically
- [ ] Use strong random strings (min 32 characters)
- [ ] Enable SSL for Neon connections in production

### Testing Requirements

**Backend testing (FastAPI):**
```python
# Use pytest with TestClient
from fastapi.testclient import TestClient

def test_create_task_authenticated():
    # Test with valid JWT token
    response = client.post(
        "/api/tasks",
        json={"title": "Test task"},
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 201

def test_create_task_unauthorized():
    # Test without token
    response = client.post("/api/tasks", json={"title": "Test"})
    assert response.status_code == 401
```

**Frontend testing (Next.js):**
- Use React Testing Library for component tests
- Test authentication flows (login, logout, protected routes)
- Test API integration with mocked responses
- Test responsive layouts at different breakpoints

**Test coverage requirements:**
- All API endpoints must have tests
- Authentication/authorization logic must be tested
- Database queries must be tested with fixtures
- Critical user flows must have integration tests

### Neon Database Best Practices

**Connection management:**
- Use connection pooling (SQLModel handles this)
- Set appropriate pool size for serverless: `pool_size=5, max_overflow=10`
- Close connections properly in FastAPI lifespan events

**Branching strategy:**
```bash
# Create branch for development
neonctl branches create --name dev

# Create branch for testing
neonctl branches create --name test --parent main

# Use branch-specific connection strings
DATABASE_URL=postgresql://...@ep-branch-name.region.aws.neon.tech/dbname
```

**Cost optimization:**
- Use autoscaling; Neon scales to zero when idle
- Optimize queries to reduce compute time
- Use appropriate indexes to minimize scan time
- Monitor usage in Neon console

### Better Auth Configuration

**Installation (Frontend):**
```bash
npm install better-auth
```

**Configuration (auth.ts):**
```typescript
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false // Set true for production
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24 // Update every 24 hours
  },
  jwt: {
    enabled: true,
    secret: process.env.BETTER_AUTH_SECRET
  }
})
```

**Backend JWT validation (FastAPI):**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return {"id": user_id, "email": payload.get("email")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Project Directory Structure

```
Phase-II/
├── frontend/                 # Next.js 16+ App Router
│   ├── app/                 # App Router pages
│   │   ├── (auth)/         # Auth-related pages
│   │   │   ├── login/
│   │   │   └── signup/
│   │   ├── (dashboard)/    # Protected dashboard pages
│   │   └── api/            # API routes (if needed)
│   ├── components/          # React components
│   ├── lib/                # Utilities and helpers
│   │   ├── auth.ts         # Better Auth configuration
│   │   └── api-client.ts   # API client with JWT
│   ├── .env.local          # Frontend environment variables
│   └── package.json
│
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── models/         # SQLModel schemas
│   │   ├── routers/        # API route handlers
│   │   ├── auth/           # JWT validation middleware
│   │   ├── database.py     # Database connection
│   │   └── config.py       # Settings management
│   ├── tests/              # Pytest tests
│   ├── .env                # Backend environment variables
│   └── requirements.txt
│
├── specs/                   # Feature specifications
├── history/                 # PHRs and ADRs
└── .specify/               # SpecKit Plus configuration
```

## Development Workflow Examples

### Example 1: Adding a New Feature (Task Management)

**Step 1: Create specification**
```bash
# User prompt: "I need to add task management with CRUD operations"
# Claude response: "I'll use /sp.specify to create the feature spec"
```

**Step 2: Generate plan**
```bash
# After spec is approved, use /sp.plan
# This will invoke the Plan agent to create architectural design
```

**Step 3: Break into tasks**
```bash
# Use /sp.tasks to generate actionable tasks
# Tasks will be ordered by dependencies
```

**Step 4: Implement**
```bash
# Use /sp.implement to execute tasks
# This will coordinate multiple agents:
# - DB Agent: Create task table schema
# - Backend Agent: Implement API endpoints
# - Frontend Agent: Build UI components
```

### Example 2: Implementing Authentication

**Correct approach (using agents):**
```
User: "Implement user authentication with Better Auth"

Claude: "I'll delegate this to the auth-security-specialist agent"
→ Uses Task tool with subagent_type="auth-security-specialist"
→ Agent designs complete auth flow
→ Agent implements signup/signin
→ Agent configures JWT validation
→ Agent tests security
```

**Incorrect approach (manual coding):**
```
❌ User: "Here's the auth code I wrote manually..."
❌ Claude: "Let me review your code..."

This violates the "No Manual Coding Policy"
```

### Example 3: Multi-Agent Coordination

**Feature: User-specific task list with filtering**

**Sequential agent invocation:**
```
1. DB Agent: Design schema
   - Create tasks table with user_id foreign key
   - Add indexes for (user_id, created_at)
   - Create migration script

2. Backend Agent: Implement API
   - POST /api/tasks (create task)
   - GET /api/tasks (list user's tasks)
   - PUT /api/tasks/{id} (update task)
   - DELETE /api/tasks/{id} (delete task)
   - Add JWT validation middleware

3. Frontend Agent: Build UI
   - Task list component with filtering
   - Task creation form
   - Task edit modal
   - Responsive layout
```

## Common Patterns

### Pattern 1: Protected API Endpoint

**Backend (FastAPI):**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.auth.jwt import get_current_user
from app.database import get_db
from app.models import Task, User

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/")
async def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tasks for authenticated user"""
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = db.exec(statement).all()
    return {"success": True, "data": tasks}

@router.post("/")
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new task for authenticated user"""
    task = Task(**task_data.dict(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return {"success": True, "data": task}
```

### Pattern 2: Frontend API Client with JWT

**Frontend (Next.js):**
```typescript
// lib/api-client.ts
import { auth } from "@/lib/auth"

export async function apiClient(endpoint: string, options: RequestInit = {}) {
  const session = await auth.getSession()

  if (!session?.token) {
    throw new Error("Not authenticated")
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${session.token}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (response.status === 401) {
    // Redirect to login
    window.location.href = '/login'
    throw new Error("Unauthorized")
  }

  return response.json()
}

// Usage in component
async function fetchTasks() {
  const data = await apiClient('/api/tasks')
  return data.data // Extract tasks from response
}
```

### Pattern 3: Database Migration with SQLModel

**Backend (migration script):**
```python
# migrations/001_create_tasks_table.py
from sqlmodel import SQLModel, create_engine
from app.models import Task, User
from app.config import settings

def upgrade():
    engine = create_engine(settings.DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    print("✓ Created tasks table with user_id foreign key")

def downgrade():
    # Drop tables if needed
    pass
```

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Missing User Filtering
```python
# WRONG: Returns all tasks from all users
@router.get("/api/tasks")
async def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()  # Security vulnerability!
    return tasks
```

### ❌ Anti-Pattern 2: Hardcoded Secrets
```python
# WRONG: Secret in code
JWT_SECRET = "my-secret-key-123"

# CORRECT: Use environment variables
from app.config import settings
JWT_SECRET = settings.JWT_SECRET_KEY
```

### ❌ Anti-Pattern 3: No Error Handling
```typescript
// WRONG: No error handling
async function createTask(data) {
  const response = await fetch('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(data)
  })
  return response.json() // What if it fails?
}

// CORRECT: Proper error handling
async function createTask(data) {
  try {
    const response = await apiClient('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(data)
    })
    if (!response.success) {
      throw new Error(response.message)
    }
    return response.data
  } catch (error) {
    console.error('Failed to create task:', error)
    throw error
  }
}
```

## Quick Reference

### Agent Selection Cheatsheet

| Task Type | Agent to Use | Example |
|-----------|-------------|---------|
| User signup/signin | `auth-security-specialist` | "Implement Better Auth signup" |
| JWT validation | `auth-security-specialist` | "Add JWT middleware to FastAPI" |
| Database schema | `neon-db-optimizer` | "Design tasks table with indexes" |
| Query optimization | `neon-db-optimizer` | "Optimize slow task list query" |
| API endpoints | `fastapi-backend` | "Create POST /api/tasks endpoint" |
| Request validation | `fastapi-backend` | "Add Pydantic validation for tasks" |
| Next.js pages | `nextjs-ui-architect` | "Build dashboard page" |
| React components | `nextjs-ui-architect` | "Create task list component" |
| Responsive design | `nextjs-ui-architect` | "Fix mobile layout issues" |

### Common Commands

```bash
# Spec-Kit Plus workflow
/sp.specify          # Create feature specification
/sp.plan            # Generate architectural plan
/sp.tasks           # Break down into tasks
/sp.implement       # Execute implementation
/sp.adr <title>     # Create architecture decision record

# Git workflow
/sp.git.commit_pr   # Commit changes and create PR

# Analysis
/sp.analyze         # Check consistency across artifacts
/sp.checklist       # Generate feature checklist
```

### Troubleshooting

**Issue: JWT token validation fails**
- Check that `BETTER_AUTH_SECRET` matches between frontend and backend
- Verify token is being sent in `Authorization: Bearer <token>` header
- Check token expiration time
- Ensure JWT algorithm matches (HS256)

**Issue: Database connection fails**
- Verify `DATABASE_URL` in .env file
- Check Neon database is running
- Ensure SSL mode is enabled for production: `?sslmode=require`
- Test connection with: `psql $DATABASE_URL`

**Issue: CORS errors in browser**
- Add frontend URL to `CORS_ORIGINS` in backend .env
- Verify FastAPI CORS middleware is configured
- Check that credentials are included in fetch requests

**Issue: User can see other users' data**
- CRITICAL SECURITY BUG: Add `user_id` filter to all queries
- Review all API endpoints for proper user isolation
- Add tests to verify users cannot access others' data

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

## Active Technologies
- Python 3.11+ (Backend), TypeScript/Node.js 18+ (Frontend) + FastAPI, SQLModel, uvicorn, python-jose, passlib (Backend); Next.js 16+, Better Auth, React 18+ (Frontend) (001-todo-web-app)
- Neon Serverless PostgreSQL with SQLModel ORM (001-todo-web-app)
- Python 3.11+ + FastAPI (latest), SQLModel (latest), python-jose[cryptography] (JWT), passlib[bcrypt] (password hashing), uvicorn (ASGI server) (002-backend-api-data)
- Neon Serverless PostgreSQL (cloud-hosted, auto-scaling) (002-backend-api-data)

## Recent Changes
- 001-todo-web-app: Added Python 3.11+ (Backend), TypeScript/Node.js 18+ (Frontend) + FastAPI, SQLModel, uvicorn, python-jose, passlib (Backend); Next.js 16+, Better Auth, React 18+ (Frontend)
