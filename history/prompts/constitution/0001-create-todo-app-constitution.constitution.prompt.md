---
id: 0001
title: Create Todo App Constitution
stage: constitution
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: PalwashaKhalid
command: /sp.constitution
labels: ["constitution", "governance", "security", "spec-driven", "multi-user"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
/sp.constitution

Project: Todo Full-Stack Web Application (Web-based, Multi-User, Authenticated)

Core principles:
- Spec-driven development (no manual coding outside generated plans)
- Security-first architecture (authentication, authorization, data isolation)
- Deterministic implementation (same spec → same behavior)
- Clear separation of concerns (auth, backend, frontend)
- Production realism (real database, real auth, real API contracts)

Key standards:
- Every feature must originate from an approved spec
- All API behavior must match the written specification exactly
- Authentication must be enforced on every API endpoint
- User data isolation is mandatory (no cross-user access possible)
- JWT verification must be stateless and deterministic
- Frontend must never trust client-side user identity without backend verification
- All database operations must be scoped to authenticated user context

Constraints:
- No manual coding (all code generated via Claude Code)
- Backend must use FastAPI + SQLModel only
- Database must be Neon Serverless PostgreSQL
- Frontend must use Next.js 16+ App Router
- Authentication must use Better Auth with JWT enabled
- Shared JWT secret must be provided via environment variables
- REST API must strictly follow documented endpoints
- All endpoints must return proper HTTP status codes

Security constraints:
- Requests without valid JWT must return 401 Unauthorized
- JWT user_id must match URL user_id or request is rejected
- Token expiration must be enforced
- Task ownership must be validated on every CRUD operation
- No sensitive secrets hardcoded in codebase

Process rules:
- Follow Agentic Dev Stack workflow:
  1. Write spec
  2. Generate implementation plan
  3. Break plan into tasks
  4. Implement via Claude Code
- Specs are the single source of truth
- Any deviation from spec requires explicit spec revision
- Each iteration must be reviewable and reproducible

Quality standards:
- API responses must be predictable and documented
- Database schema must support multi-user scalability
- Frontend must be responsive (mobile + desktop)
- Error handling must be explicit and user-safe
- Code must be readable and logically structured

Success criteria:
- All 5 basic Todo features implemented as a web app
- Secure multi-user authentication fully functional
- Users can only see and modify their own tasks
- Frontend, backend, and database work together seamlessly
- Application runs end-to-end with real auth and persistent storage
- Project is fully spec-compliant and review-ready for hackathon judging
```

## Response snapshot

Created comprehensive project constitution (v1.0.0) for Todo Full-Stack Web Application with 5 core principles:

1. **Spec-Driven Development (NON-NEGOTIABLE)**: All code generated through Agentic Dev Stack workflow (spec → plan → tasks → implement). Manual coding prohibited.

2. **Security-First Architecture (NON-NEGOTIABLE)**: Authentication/authorization mandatory on all endpoints. JWT verification, user data isolation, no cross-user access.

3. **Deterministic Implementation**: Same spec produces same behavior. Predictable APIs, documented errors, reproducible schemas.

4. **Clear Separation of Concerns**: Distinct layers - Better Auth (auth), FastAPI (backend), Next.js (frontend), Neon (database).

5. **Production Realism**: Real database, real auth, real API contracts. No mocks or shortcuts.

Constitution includes:
- Mandatory technology stack (Next.js 16+, FastAPI, SQLModel, Neon, Better Auth)
- Security requirements with JWT flow and validation checklist
- Process rules enforcing Agentic Dev Stack workflow
- Quality standards for API, database, frontend, and code readability
- Success criteria for hackathon completion
- Governance rules for amendments and compliance

All templates reviewed for consistency. No placeholders remaining.

## Outcome

- ✅ Impact: Established formal governance for Todo web application project. All development must follow constitution principles.
- 🧪 Tests: None (documentation task)
- 📁 Files: Created .specify/memory/constitution.md (316 lines)
- 🔁 Next prompts: /sp.specify to create first feature specification following constitution principles
- 🧠 Reflection: Constitution provides clear guardrails for multi-user security, spec-driven workflow, and technology stack constraints. Ready for feature development.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (constitution creation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification for authentication or task management following constitution workflow
