---
id: 0003
title: Create Todo App Constitution
stage: constitution
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-todo-web-app
user: PalwashaKhalid
command: /sp.constitution
labels: ["constitution", "security", "spec-driven-development", "agentic-workflow", "multi-user"]
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

Created comprehensive constitution (v1.0.0) for Todo Full-Stack Web Application with 5 core principles:

**I. Spec-Driven Development (NON-NEGOTIABLE)**
- All code generated through Agentic Dev Stack workflow (spec → plan → tasks → implement)
- Manual coding prohibited
- Specifications are single source of truth

**II. Security-First Architecture (NON-NEGOTIABLE)**
- Authentication enforced on all protected endpoints
- User data isolation mandatory (no cross-user access)
- JWT verification stateless and deterministic
- All database operations scoped to authenticated user

**III. Deterministic Implementation**
- Same spec produces same behavior across environments
- API responses predictable and documented
- Error handling explicit with documented status codes

**IV. Clear Separation of Concerns**
- Authentication layer: Better Auth + JWT
- Backend layer: FastAPI + SQLModel
- Frontend layer: Next.js App Router
- Communication through REST API contracts

**V. Production Realism**
- Real database (Neon Serverless PostgreSQL)
- Real authentication (Better Auth with JWT)
- Real API contracts (OpenAPI documented)
- Real error handling and connection management

**Additional sections:**
- Technology Stack (mandatory, no substitutions)
- Security Requirements (authentication flow, validation checklist, forbidden patterns)
- Process Rules (Agentic Dev Stack workflow, spec compliance, agent delegation)
- Quality Standards (API, database, frontend, code readability)
- Success Criteria (functional, security, integration, quality, production readiness)
- Governance (amendment process, compliance review, complexity justification)

**Template consistency verified:**
- ✅ spec-template.md - Compatible with constitution requirements
- ✅ plan-template.md - Constitution Check section aligns with principles
- ✅ tasks-template.md - User story organization supports spec-driven workflow

**Sync Impact Report prepended to constitution file documenting:**
- Version: 1.0.0 (initial constitution)
- Rationale: First formal constitution for hackathon project
- 5 principles defined with clear rules and rationale
- 6 major sections added (Technology Stack, Security, Process, Quality, Success, Governance)
- All templates reviewed and confirmed compatible

## Outcome

- ✅ Impact: Constitution v1.0.0 created with 5 core principles, mandatory technology stack, security requirements, process rules, quality standards, and governance framework. All dependent templates verified for consistency.
- 🧪 Tests: N/A (documentation artifact - no executable tests required)
- 📁 Files: Modified 1 file (.specify/memory/constitution.md) - 316 lines, comprehensive coverage of all project requirements
- 🔁 Next prompts: Ready for feature specification creation via /sp.specify. Constitution establishes foundation for spec-driven development workflow.
- 🧠 Reflection: Constitution successfully captures all hackathon requirements including multi-user authentication, data isolation, and production-grade technology stack. Security-first and spec-driven principles are non-negotiable, ensuring project meets judging criteria.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution creation completed successfully with all placeholders resolved
- Graders run and results (PASS/FAIL): PASS - All validation checks passed (no unresolved placeholders, proper versioning, ISO dates, declarative principles)
- Prompt variant (if applicable): Standard /sp.constitution command with comprehensive project requirements
- Next experiment (smallest change to try): Monitor constitution compliance during first feature implementation to validate that principles are practical and enforceable
