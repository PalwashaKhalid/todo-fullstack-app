# Research: Todo Full-Stack Web Application

**Feature**: 001-todo-web-app
**Date**: 2026-02-05
**Phase**: Phase 0 - Research & Architecture Decisions

## Executive Summary

This document captures the research, technology decisions, and architectural rationale for transforming a console-based Todo application into a secure, multi-user web application. All decisions align with the project constitution's core principles: spec-driven development, security-first architecture, deterministic implementation, clear separation of concerns, and production realism.

---

## Technology Stack Decisions

### Backend: Python FastAPI + SQLModel

**Decision**: Use FastAPI as the backend framework with SQLModel as the ORM.

**Rationale**:
- **Performance**: FastAPI is one of the fastest Python frameworks, built on Starlette and Pydantic
- **Async Support**: Native async/await support for handling concurrent requests efficiently
- **Type Safety**: Pydantic models provide runtime validation and type checking
- **SQLModel Integration**: Combines Pydantic and SQLAlchemy for type-safe database operations
- **OpenAPI Documentation**: Automatic API documentation generation (Swagger UI)
- **Developer Experience**: Excellent error messages and IDE support

**Alternatives Considered**:
- **Django REST Framework**: More batteries-included but heavier, slower, and less modern async support
- **Flask**: Simpler but lacks built-in async support and type safety
- **Node.js/Express**: Would require JavaScript on backend, losing Python's data science ecosystem

**Trade-offs**:
- ✅ High performance and modern async patterns
- ✅ Type safety reduces runtime errors
- ✅ Automatic API documentation
- ⚠️ Smaller ecosystem than Django (acceptable for this project scope)

---

### Frontend: Next.js 16+ (App Router)

**Decision**: Use Next.js 16+ with App Router for the frontend.

**Rationale**:
- **React Server Components**: Modern architecture with server-side rendering
- **App Router**: File-based routing with layouts and nested routes
- **Performance**: Automatic code splitting, image optimization, font optimization
- **Developer Experience**: Hot module replacement, TypeScript support, built-in CSS support
- **Production Ready**: Used by major companies (Vercel, Netflix, TikTok)
- **Better Auth Compatibility**: Excellent integration with Better Auth library

**Alternatives Considered**:
- **Create React App**: Deprecated, no SSR, worse performance
- **Vite + React**: Good DX but requires more configuration for SSR
- **Vue.js/Nuxt**: Different ecosystem, team may not be familiar
- **Svelte/SvelteKit**: Smaller ecosystem, less mature

**Trade-offs**:
- ✅ Best-in-class performance and DX
- ✅ Server components reduce client bundle size
- ✅ Built-in optimizations (images, fonts, code splitting)
- ⚠️ App Router is newer (less Stack Overflow answers) - acceptable, well-documented

---

### Database: Neon Serverless PostgreSQL

**Decision**: Use Neon as the PostgreSQL database provider.

**Rationale**:
- **Serverless**: Auto-scaling, scales to zero when idle (cost-effective)
- **PostgreSQL**: Industry-standard relational database with ACID guarantees
- **Branching**: Database branching for development/staging environments
- **Performance**: Connection pooling, read replicas, fast cold starts
- **Developer Experience**: Simple setup, no infrastructure management
- **Cost**: Free tier available, pay-per-use pricing

**Alternatives Considered**:
- **Supabase**: Good but more opinionated (includes auth, storage, realtime)
- **PlanetScale**: MySQL-based, different SQL dialect
- **AWS RDS**: Requires more infrastructure management, not serverless
- **MongoDB**: NoSQL, loses relational guarantees and SQL familiarity

**Trade-offs**:
- ✅ True serverless with auto-scaling
- ✅ PostgreSQL compatibility (mature ecosystem)
- ✅ Database branching for safe testing
- ⚠️ Vendor lock-in (mitigated by standard PostgreSQL compatibility)

---

### Authentication: Better Auth + JWT

**Decision**: Use Better Auth library with JWT token authentication.

**Rationale**:
- **Modern**: Built specifically for Next.js App Router and React Server Components
- **JWT Support**: Native JWT token generation and validation
- **Type Safety**: Full TypeScript support with type-safe APIs
- **Flexibility**: Supports multiple auth strategies (email/password, OAuth, magic links)
- **Database Agnostic**: Works with PostgreSQL, MySQL, SQLite
- **Stateless**: JWT tokens enable stateless authentication (scalable)

**Alternatives Considered**:
- **NextAuth.js**: More mature but complex configuration, session-based by default
- **Auth0**: Third-party service, adds external dependency and cost
- **Clerk**: Proprietary, expensive for production
- **Custom JWT**: Reinventing the wheel, security risks

**Trade-offs**:
- ✅ Modern, built for Next.js App Router
- ✅ JWT tokens enable stateless backend authentication
- ✅ Type-safe APIs reduce errors
- ⚠️ Newer library (less community content) - acceptable, good documentation

---

## Architecture Decisions

### Decision 1: Stateless JWT Authentication

**Context**: Multi-user application requires secure authentication and authorization.

**Decision**: Use JWT tokens for stateless authentication between frontend and backend.

**Rationale**:
- **Scalability**: No server-side session storage required
- **Separation**: Frontend and backend can scale independently
- **Security**: Tokens are signed and verified cryptographically
- **Expiration**: Built-in token expiration for security
- **User Identity**: Token payload contains user ID for data filtering

**Implementation**:
1. User signs in via Better Auth on frontend
2. Better Auth issues JWT token with user ID in payload
3. Frontend includes token in `Authorization: Bearer <token>` header
4. Backend validates token signature using shared secret
5. Backend extracts user ID from token for data filtering

**Alternatives Rejected**:
- **Session-based auth**: Requires shared session store (Redis), adds complexity
- **Cookie-based auth**: CSRF concerns, harder to use with mobile apps later

**Trade-offs**:
- ✅ Stateless, scalable, no session storage needed
- ✅ Works across domains (CORS-friendly)
- ⚠️ Token revocation requires additional logic (acceptable for MVP)

---

### Decision 2: Monorepo Structure (Backend + Frontend)

**Context**: Web application with separate backend and frontend codebases.

**Decision**: Use monorepo structure with `backend/` and `frontend/` directories at repository root.

**Rationale**:
- **Simplicity**: Single repository for all code
- **Atomic Changes**: Frontend and backend changes in same commit
- **Shared Configuration**: Single .gitignore, single CI/CD pipeline
- **Development**: Easy to run both services locally

**Structure**:
```
Phase-II/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── auth/
│   │   └── database.py
│   ├── tests/
│   ├── .env
│   └── requirements.txt
├── frontend/         # Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── .env.local
│   └── package.json
└── specs/           # Documentation
```

**Alternatives Rejected**:
- **Separate repositories**: Harder to coordinate changes, more complex deployment
- **Single codebase**: Mixing Python and TypeScript in same directory structure is messy

**Trade-offs**:
- ✅ Simple to manage, single source of truth
- ✅ Atomic commits across frontend and backend
- ⚠️ Larger repository size (acceptable for this project scale)

---

### Decision 3: User Data Isolation via Database Filtering

**Context**: Multi-user application must prevent users from accessing each other's data.

**Decision**: Filter all database queries by authenticated user's ID extracted from JWT token.

**Rationale**:
- **Security**: Defense in depth - every query is scoped to user
- **Simplicity**: No complex permission system needed
- **Performance**: Database indexes on user_id enable fast filtering
- **Deterministic**: Same user always sees same data

**Implementation Pattern**:
```python
@router.get("/api/tasks")
async def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ALWAYS filter by user_id from JWT token
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks
```

**Alternatives Rejected**:
- **Row-level security (RLS)**: Database-level but adds complexity
- **Application-level permissions**: Overkill for single-owner model

**Trade-offs**:
- ✅ Simple, explicit, auditable
- ✅ Fast with proper indexes
- ✅ Impossible to accidentally leak data
- ⚠️ Requires discipline (every query must filter) - mitigated by code review

---

### Decision 4: RESTful API Design

**Context**: Frontend and backend communicate via HTTP API.

**Decision**: Use RESTful API conventions with standard HTTP methods and status codes.

**Rationale**:
- **Standard**: Well-understood conventions
- **Predictable**: Consistent patterns across all endpoints
- **Tooling**: Works with standard HTTP clients, testing tools
- **Documentation**: OpenAPI/Swagger auto-generation

**Conventions**:
- `GET /api/tasks` - List user's tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PATCH /api/tasks/{id}/status` - Update task status

**Status Codes**:
- 200: Success (GET, PUT, PATCH)
- 201: Created (POST)
- 204: No Content (DELETE)
- 400: Bad Request (validation errors)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (valid token, insufficient permissions)
- 404: Not Found
- 500: Internal Server Error

**Alternatives Rejected**:
- **GraphQL**: Overkill for simple CRUD, adds complexity
- **gRPC**: Not web-friendly, requires protobuf compilation
- **Custom RPC**: Reinventing the wheel

**Trade-offs**:
- ✅ Standard, well-understood, predictable
- ✅ Works with all HTTP clients
- ✅ Automatic documentation generation
- ⚠️ Less flexible than GraphQL (acceptable for this use case)

---

## Security Considerations

### JWT Token Security

**Threats Mitigated**:
- **Token Forgery**: Tokens are cryptographically signed with HS256
- **Token Theft**: HTTPS in production, short expiration times
- **Replay Attacks**: Token expiration enforced
- **User Impersonation**: User ID embedded in signed token payload

**Security Measures**:
- Minimum 32-character secret key (high entropy)
- Token expiration (30 minutes default)
- HTTPS only in production
- Secrets in environment variables (never committed)
- Token validation on every protected endpoint

### Data Isolation Security

**Threats Mitigated**:
- **Horizontal Privilege Escalation**: User cannot access other users' tasks
- **Direct Object Reference**: Task ID alone is insufficient, user_id must match
- **SQL Injection**: SQLModel/SQLAlchemy parameterized queries

**Security Measures**:
- Every query filtered by authenticated user's ID
- Authorization checks on update/delete operations (403 if user doesn't own resource)
- Database foreign key constraints enforce referential integrity
- Input validation via Pydantic models

### Password Security

**Threats Mitigated**:
- **Password Theft**: Passwords hashed with bcrypt (never stored plaintext)
- **Rainbow Tables**: Bcrypt includes salt automatically
- **Brute Force**: Bcrypt is intentionally slow (computational cost)

**Security Measures**:
- Bcrypt hashing via passlib
- Minimum password length (8 characters)
- Passwords never logged or returned in API responses

---

## Performance Considerations

### Database Performance

**Optimizations**:
- Index on `user_id` column for fast filtering
- Composite index on `(user_id, created_at)` for sorted queries
- Connection pooling via SQLModel/SQLAlchemy
- Neon auto-scaling handles load spikes

**Expected Performance**:
- Task list query: <50ms (indexed user_id lookup)
- Task creation: <100ms (single INSERT)
- Task update/delete: <50ms (indexed lookup + UPDATE/DELETE)

### Frontend Performance

**Optimizations**:
- Next.js automatic code splitting
- Server components reduce client bundle size
- Image optimization via next/image
- Font optimization via next/font

**Expected Performance**:
- First Contentful Paint: <1.5s
- Time to Interactive: <3s
- Lighthouse score: >90

---

## Scalability Considerations

### Horizontal Scalability

**Backend**:
- Stateless JWT authentication enables multiple backend instances
- No shared session state required
- Database connection pooling per instance

**Frontend**:
- Static assets can be CDN-cached
- Server components reduce client-side JavaScript
- Next.js supports edge deployment

**Database**:
- Neon auto-scales compute based on load
- Read replicas available for read-heavy workloads
- Connection pooling prevents connection exhaustion

### Vertical Scalability

**Limits**:
- Single user: 10,000+ tasks (acceptable)
- System: 100+ concurrent users (acceptable for MVP)
- Database: Neon handles up to 10,000 connections

---

## Development Workflow

### Agentic Dev Stack

**Process**:
1. **Specify** (`/sp.specify`) - Create feature specification with user stories
2. **Plan** (`/sp.plan`) - Generate architectural plan and design documents
3. **Tasks** (`/sp.tasks`) - Break down into actionable tasks
4. **Implement** (`/sp.implement`) - Execute tasks via specialized agents

**Agents**:
- **auth-security-specialist**: Authentication, JWT, Better Auth, security
- **fastapi-backend**: API endpoints, validation, business logic
- **nextjs-ui-architect**: Frontend pages, components, responsive design
- **neon-db-optimizer**: Database schema, queries, indexes, migrations

### No Manual Coding Policy

**Enforcement**:
- All code generated via Claude Code
- Manual edits violate constitution
- Changes require spec amendment and regeneration

**Rationale**:
- Ensures traceability and auditability
- Prevents undocumented behavior
- Aligns with hackathon judging criteria

---

## Risk Analysis

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| JWT secret leaked | Low | High | Environment variables, never commit, rotate regularly |
| Database connection exhaustion | Low | Medium | Connection pooling, Neon auto-scaling |
| CORS misconfiguration | Medium | Medium | Explicit CORS origins in config, test cross-origin |
| Token expiration UX issues | Medium | Low | Clear error messages, redirect to login |
| Better Auth breaking changes | Low | Medium | Pin version, test before upgrading |

### Security Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| User data leakage | Low | Critical | Every query filtered by user_id, authorization checks |
| XSS attacks | Medium | High | Input sanitization, React auto-escaping |
| SQL injection | Low | High | Parameterized queries via SQLModel |
| Brute force login | Medium | Medium | Rate limiting (future), bcrypt slow hashing |
| Session hijacking | Low | High | HTTPS only, short token expiration |

### Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Neon service outage | Low | High | Monitor status page, have backup plan |
| Deployment failures | Medium | Medium | Test in staging, rollback plan |
| Environment variable misconfiguration | Medium | High | Validation on startup, clear error messages |
| Database migration failures | Low | High | Test migrations in dev, backup before production |

---

## Open Questions & Future Considerations

### Deferred Features

- Email verification (not required for MVP)
- Password reset flow (not required for MVP)
- Rate limiting (not required for MVP)
- Task search and filtering (not required for MVP)
- Real-time updates (not required for MVP)

### Future Enhancements

- OAuth providers (Google, GitHub)
- Task sharing between users
- Task categories and tags
- Due dates and reminders
- Mobile native applications
- Offline-first functionality

### Monitoring & Observability

- Application logging (structured logs)
- Error tracking (Sentry or similar)
- Performance monitoring (APM)
- Database query performance
- User analytics

---

## Conclusion

This research document captures the key technology decisions and architectural rationale for the Todo Full-Stack Web Application. All decisions align with the constitution's core principles and prioritize security, scalability, and developer experience. The chosen stack (FastAPI + SQLModel + Next.js + Better Auth + Neon) provides a modern, production-ready foundation for building a secure multi-user web application.

**Next Steps**: Proceed to implementation via `/sp.implement` following the tasks defined in tasks.md.
