---
id: 0002
title: Create Todo App Constitution
stage: constitution
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-todo-web-app
user: PalwashaKhalid
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
  - N/A (documentation artifact)
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

Created comprehensive constitution for Todo Full-Stack Web Application with 5 core principles:

1. **Spec-Driven Development (NON-NEGOTIABLE)**: All code must be generated through Agentic Dev Stack workflow (spec → plan → tasks → implement). Manual coding prohibited.

2. **Security-First Architecture (NON-NEGOTIABLE)**: Authentication and authorization mandatory on all protected resources. JWT verification, user data isolation, and token validation enforced.

3. **Deterministic Implementation**: Same specification produces same behavior across all implementations and environments.

4. **Clear Separation of Concerns**: Distinct boundaries between authentication (Better Auth + JWT), backend (FastAPI + SQLModel), and frontend (Next.js App Router).

5. **Production Realism**: All components use production-grade technologies - real database (Neon), real auth (Better Auth), real API contracts.

Constitution includes:
- Mandatory technology stack table with rationale
- Security requirements with authentication flow and validation checklist
- Process rules enforcing Agentic Dev Stack workflow
- Quality standards for API, database, frontend, and code readability
- Success criteria for functional, security, integration, quality, and production readiness
- Governance section with amendment process and compliance review

Version 1.0.0 ratified on 2026-02-05. All templates reviewed for compatibility. Sync Impact Report prepended to constitution file.

## Outcome

- ✅ Impact: Constitution established as authoritative governance document for project. All development must comply with 5 core principles. Security-first architecture and spec-driven workflow now mandatory.
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md (316 lines)
- 🔁 Next prompts: /sp.specify to create first feature specification following constitution principles
- 🧠 Reflection: Constitution successfully captures all project requirements including security constraints, technology stack mandates, and quality standards. Clear separation between NON-NEGOTIABLE principles (Spec-Driven, Security-First) and supporting principles ensures focus on critical requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution created successfully with all placeholders resolved
- Graders run and results (PASS/FAIL): PASS - All templates reviewed and compatible with constitution requirements
- Prompt variant (if applicable): N/A (initial constitution creation)
- Next experiment (smallest change to try): Test constitution enforcement by creating first feature spec and validating compliance with principles
