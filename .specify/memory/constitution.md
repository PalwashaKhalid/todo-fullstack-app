<!--
Sync Impact Report:
- Version: 1.0.0 (Initial constitution)
- Rationale: First formal constitution for Todo Full-Stack Web Application
- Principles defined: 5 core principles
- Sections added: Technology Stack, Security Requirements, Process Rules, Quality Standards
- Templates status:
  ✅ spec-template.md - Reviewed, compatible with constitution requirements
  ✅ plan-template.md - Reviewed, Constitution Check section aligns with principles
  ✅ tasks-template.md - Reviewed, user story organization supports spec-driven workflow
- Follow-up: None - all placeholders resolved
- Date: 2026-02-05
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code MUST be generated through the Agentic Dev Stack workflow. Manual coding is prohibited.

**Rules:**
- Every feature originates from an approved specification document
- Implementation follows: spec → plan → tasks → implement cycle
- Specifications are the single source of truth for all behavior
- Any deviation from spec requires explicit spec revision and re-approval
- Each iteration must be reviewable, reproducible, and traceable

**Rationale:** Ensures consistency, auditability, and alignment with hackathon judging criteria. Prevents scope creep and undocumented behavior changes.

### II. Security-First Architecture (NON-NEGOTIABLE)

Security is mandatory at every layer. Authentication and authorization MUST be enforced on all protected resources.

**Rules:**
- Authentication MUST be enforced on every API endpoint (except public auth endpoints)
- User data isolation is mandatory - no cross-user data access possible
- JWT verification MUST be stateless and deterministic
- Frontend MUST never trust client-side user identity without backend verification
- All database operations MUST be scoped to authenticated user context
- Requests without valid JWT MUST return 401 Unauthorized
- JWT user_id MUST match URL/request user_id or request is rejected with 403 Forbidden
- Token expiration MUST be enforced
- Resource ownership MUST be validated on every CRUD operation
- No sensitive secrets hardcoded in codebase - environment variables only

**Rationale:** Multi-user applications require strict security boundaries. Data leaks between users are unacceptable and would fail security review.

### III. Deterministic Implementation

Same specification MUST produce same behavior across all implementations and environments.

**Rules:**
- All API behavior MUST match written specification exactly
- API responses MUST be predictable and documented
- Error handling MUST be explicit with documented status codes
- Database schema MUST be version-controlled and reproducible
- Environment-specific behavior MUST be isolated to configuration only

**Rationale:** Enables reliable testing, debugging, and deployment. Reduces "works on my machine" issues.

### IV. Clear Separation of Concerns

Architecture MUST maintain distinct boundaries between authentication, backend logic, and frontend presentation.

**Rules:**
- Authentication layer handles only auth/authz concerns (Better Auth + JWT)
- Backend layer handles only business logic and data access (FastAPI + SQLModel)
- Frontend layer handles only presentation and user interaction (Next.js App Router)
- Each layer communicates through well-defined contracts (REST API)
- No business logic in frontend; no presentation logic in backend
- Database access only through backend ORM (SQLModel)

**Rationale:** Enables independent testing, parallel development, and clear responsibility boundaries. Simplifies debugging and maintenance.

### V. Production Realism

All components MUST use production-grade technologies and patterns, not mocks or shortcuts.

**Rules:**
- Real database (Neon Serverless PostgreSQL) - no in-memory or file-based storage
- Real authentication (Better Auth with JWT) - no hardcoded users or bypass modes
- Real API contracts (OpenAPI/Swagger documented) - no undocumented endpoints
- Real error handling - no silent failures or generic error messages
- Real connection management - proper pooling, timeouts, and cleanup

**Rationale:** Demonstrates production readiness for hackathon judging. Ensures application can scale beyond demo scenarios.

## Technology Stack

**MANDATORY - No substitutions allowed:**

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Frontend | Next.js App Router | 16+ | Modern React framework with server components |
| Backend | Python FastAPI | Latest | High-performance async API framework |
| ORM | SQLModel | Latest | Type-safe Pydantic + SQLAlchemy integration |
| Database | Neon Serverless PostgreSQL | Latest | Serverless, auto-scaling, branch-friendly |
| Authentication | Better Auth | Latest | Modern auth with JWT support for Next.js |
| Development | Claude Code + Spec-Kit Plus | Latest | Agentic development workflow enforcement |

**Justification for constraints:**
- Stack chosen for hackathon compatibility and judging criteria
- All technologies support multi-user, authenticated, persistent storage requirements
- No manual coding policy requires Claude Code + Spec-Kit Plus
- Better Auth provides JWT tokens that FastAPI can verify with shared secret

## Security Requirements

### Authentication Flow (MANDATORY)

**Better Auth with JWT:**
1. User logs in on Frontend → Better Auth creates session and issues JWT token
2. Frontend makes API call → Includes JWT in `Authorization: Bearer <token>` header
3. Backend receives request → Extracts token from header, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID, email, etc.
5. Backend filters data → Returns only resources belonging to authenticated user

### Security Validation Checklist

Every protected endpoint MUST pass:
- [ ] JWT token present in Authorization header
- [ ] JWT signature valid (verified with BETTER_AUTH_SECRET)
- [ ] JWT not expired
- [ ] User ID extracted from token payload
- [ ] User ID matches resource owner or request context
- [ ] Database query filtered by user_id
- [ ] Response contains only user's own data

### Forbidden Patterns

**NEVER:**
- Hardcode JWT secrets or database credentials
- Trust user_id from request body/query params without JWT verification
- Return data without user_id filtering
- Skip authentication checks for "convenience"
- Use weak secrets (minimum 32 characters required)
- Commit .env files to version control

## Process Rules

### Agentic Dev Stack Workflow (MANDATORY)

**All development MUST follow:**

1. **Specify** (`/sp.specify`): Create feature specification
   - Define user stories with acceptance criteria
   - Document functional requirements
   - Establish success criteria
   - Get user approval before proceeding

2. **Plan** (`/sp.plan`): Generate architectural plan
   - Design technical approach
   - Define API contracts
   - Plan database schema
   - Document architecture decisions
   - Get user approval before proceeding

3. **Tasks** (`/sp.tasks`): Break down into actionable tasks
   - Generate dependency-ordered task list
   - Organize by user story for independent testing
   - Include acceptance criteria per task
   - Identify parallel execution opportunities

4. **Implement** (`/sp.implement`): Execute via Claude Code
   - Coordinate specialized agents (Auth, Backend, Frontend, DB)
   - Generate all code through agents
   - Validate against spec at each step
   - Create PHR (Prompt History Record) for traceability

### Spec Compliance

- Specifications are immutable once approved
- Implementation MUST match spec exactly
- Discovered issues require spec amendment, not implementation workarounds
- All changes must be traceable through PHRs and ADRs

### Agent Delegation

**Use specialized agents for domain-specific work:**
- **auth-security-specialist**: Authentication, JWT, Better Auth, security audits
- **fastapi-backend**: API endpoints, validation, business logic
- **nextjs-ui-architect**: Frontend pages, components, responsive design
- **neon-db-optimizer**: Database schema, queries, indexes, migrations

## Quality Standards

### API Standards

**REST Endpoint Conventions:**
- Use plural nouns: `/api/tasks`, `/api/users`
- Include resource IDs in path: `/api/tasks/{task_id}`
- Use HTTP methods correctly: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)

**Response Format:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "errors": []
}
```

**Status Codes (MANDATORY):**
- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (valid token, insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

### Database Standards

**All user-owned tables MUST include:**
- `id`: Primary key (auto-increment)
- `user_id`: Foreign key to users table (indexed)
- `created_at`: Timestamp (UTC, auto-set)
- `updated_at`: Timestamp (UTC, auto-update)

**Index Strategy:**
- Always index `user_id` for fast filtering
- Add composite indexes for common query patterns: `(user_id, created_at)`
- Avoid over-indexing (Neon autoscales; optimize for query patterns)

### Frontend Standards

**Responsive Design:**
- Mobile-first approach
- Test at breakpoints: 320px, 768px, 1024px, 1440px
- Touch-friendly targets (minimum 44x44px)

**Error Handling:**
- Display user-friendly messages for 400/401/403 errors
- Redirect to login on 401
- Show validation errors inline on forms
- Log 500 errors and show generic message to user

### Code Readability

- Clear variable and function names
- Logical file organization per layer
- Consistent formatting (enforced by linters)
- Comments only where logic is non-obvious
- No dead code or commented-out blocks

## Success Criteria

**Project is complete when:**

1. **Functional Completeness:**
   - All 5 basic Todo features implemented as web application
   - Users can signup, signin, and manage their own tasks
   - Full CRUD operations on tasks (Create, Read, Update, Delete)
   - Data persists in Neon PostgreSQL database

2. **Security Validation:**
   - Multi-user authentication fully functional
   - Users can ONLY see and modify their own tasks
   - JWT validation working on all protected endpoints
   - No cross-user data leakage possible

3. **Integration Validation:**
   - Frontend, backend, and database work together seamlessly
   - API contracts match specification exactly
   - Error handling works end-to-end
   - Application runs without manual intervention

4. **Quality Validation:**
   - Application is spec-compliant and traceable
   - All code generated through Agentic Dev Stack workflow
   - PHRs document all development decisions
   - Project is review-ready for hackathon judging

5. **Production Readiness:**
   - Real authentication with Better Auth + JWT
   - Real database with Neon Serverless PostgreSQL
   - Proper error handling and status codes
   - Environment variables for all secrets
   - Responsive frontend works on mobile and desktop

## Governance

### Amendment Process

1. Proposed changes MUST be documented with rationale
2. Impact analysis MUST identify affected templates and code
3. Version MUST be incremented per semantic versioning:
   - **MAJOR**: Backward incompatible principle changes
   - **MINOR**: New principles or sections added
   - **PATCH**: Clarifications, wording fixes, non-semantic changes
4. All dependent templates MUST be updated for consistency
5. Sync Impact Report MUST be prepended to constitution file

### Compliance Review

- All PRs MUST verify compliance with constitution principles
- Spec deviations MUST be rejected or require spec amendment
- Security violations MUST block merge
- Manual coding MUST be rejected (except emergency fixes with explicit approval)

### Complexity Justification

Any violation of constitution principles MUST be justified in plan.md Complexity Tracking section:
- What principle is violated
- Why the violation is necessary
- What simpler alternative was rejected and why

### Living Document

This constitution supersedes all other development practices. When conflicts arise, constitution takes precedence. Use CLAUDE.md for runtime development guidance and agent delegation rules.

**Version**: 1.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05
