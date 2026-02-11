---
id: 0004
title: Create Todo App Constitution
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-todo-web-app
user: developer
command: /sp.constitution
labels: ["constitution", "governance", "principles", "security", "spec-driven"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
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

Created constitution v1.0.0 for Todo Full-Stack Web Application with 5 core principles:

1. **Spec-Driven Development (NON-NEGOTIABLE)**: All code generated through Agentic Dev Stack workflow (spec → plan → tasks → implement). Manual coding prohibited.

2. **Security-First Architecture (NON-NEGOTIABLE)**: Authentication enforced on all protected endpoints. User data isolation mandatory. JWT verification stateless and deterministic.

3. **Deterministic Implementation**: Same spec produces same behavior. API responses predictable and documented.

4. **Clear Separation of Concerns**: Auth layer (Better Auth + JWT), Backend layer (FastAPI + SQLModel), Frontend layer (Next.js App Router) with well-defined REST API contracts.

5. **Production Realism**: Real database (Neon), real authentication (Better Auth), real API contracts. No mocks or shortcuts.

Additional sections established:
- **Technology Stack**: Mandatory stack defined (Next.js 16+, FastAPI, SQLModel, Neon, Better Auth)
- **Security Requirements**: JWT authentication flow with validation checklist
- **Process Rules**: Agentic Dev Stack workflow enforcement
- **Quality Standards**: API conventions, database standards, frontend requirements
- **Success Criteria**: 5-point validation for project completion
- **Governance**: Amendment process, compliance review, complexity justification

All dependent templates verified for consistency:
- ✅ spec-template.md - Compatible with constitution requirements
- ✅ plan-template.md - Constitution Check section aligns with principles
- ✅ tasks-template.md - User story organization supports spec-driven workflow

## Outcome

- ✅ Impact: Established formal governance framework for Todo Full-Stack Web Application. All future development must comply with 5 core principles. Security-first architecture and spec-driven workflow now mandatory.
- 🧪 Tests: N/A (governance document, not code)
- 📁 Files: Created .specify/memory/constitution.md (316 lines) with Sync Impact Report
- 🔁 Next prompts: Ready for /sp.specify to create first feature specification following constitution principles
- 🧠 Reflection: Constitution successfully captures all user requirements including security constraints, technology stack mandates, and process rules. No placeholders remaining. All principles are testable and enforceable.

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders resolved, templates verified for consistency
- Graders run and results (PASS/FAIL): PASS - Constitution complete with no unresolved tokens, version 1.0.0 established
- Prompt variant (if applicable): Standard /sp.constitution workflow
- Next experiment (smallest change to try): Begin feature specification with /sp.specify to validate constitution principles in practice
