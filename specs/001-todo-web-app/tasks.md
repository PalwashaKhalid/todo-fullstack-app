# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-todo-web-app/`
**Prerequisites**: spec.md (user stories with priorities P1-P5)

**Tests**: Not explicitly requested in specification - test tasks omitted per template guidelines

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/app/`, `frontend/app/`, `frontend/components/`, `frontend/lib/`
- Backend uses FastAPI + SQLModel
- Frontend uses Next.js 16+ App Router

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure with app/, tests/, .env, requirements.txt
- [x] T002 Create frontend directory structure with app/, components/, lib/, .env.local, package.json
- [x] T003 [P] Initialize Python virtual environment and install FastAPI, SQLModel, uvicorn, python-jose, passlib, python-multipart in backend/requirements.txt
- [x] T004 [P] Initialize Next.js 16+ project with TypeScript and install better-auth, tailwindcss in frontend/
- [x] T005 [P] Create backend/.env template with DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, BETTER_AUTH_SECRET, CORS_ORIGINS
- [x] T006 [P] Create frontend/.env.local template with BETTER_AUTH_SECRET, NEXT_PUBLIC_API_URL, DATABASE_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Setup Neon database connection in backend/app/database.py with SQLModel engine and session management
- [x] T008 Create User model in backend/app/models/user.py with id, email (unique), hashed_password, created_at fields
- [x] T009 Create database initialization script in backend/app/database.py to create all tables
- [x] T010 [P] Implement password hashing utilities in backend/app/auth/password.py using passlib with bcrypt
- [x] T011 [P] Implement JWT token creation and validation in backend/app/auth/jwt.py using python-jose
- [x] T012 [P] Create JWT authentication dependency in backend/app/auth/dependencies.py with get_current_user function
- [x] T013 Create FastAPI main application in backend/app/main.py with CORS middleware configuration
- [x] T014 Create settings/config management in backend/app/config.py using pydantic BaseSettings
- [x] T015 [P] Setup Better Auth configuration in frontend/lib/auth.ts with PostgreSQL provider and JWT enabled
- [x] T016 [P] Create API client utility in frontend/lib/api-client.ts with JWT token injection and error handling

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, sign in, and access protected pages with JWT authentication

**Independent Test**: Create an account, sign out, sign back in, verify protected pages require authentication

### Implementation for User Story 1

- [x] T017 [P] [US1] Create auth router in backend/app/routers/auth.py with signup endpoint (POST /api/auth/signup)
- [x] T018 [P] [US1] Implement signin endpoint in backend/app/routers/auth.py (POST /api/auth/signin) returning JWT token
- [x] T019 [P] [US1] Implement signout endpoint in backend/app/routers/auth.py (POST /api/auth/signout)
- [x] T020 [US1] Register auth router in backend/app/main.py
- [x] T021 [US1] Add email validation and duplicate email check in signup endpoint
- [x] T022 [US1] Add password strength validation in signup endpoint (minimum 8 characters)
- [x] T023 [P] [US1] Create signup page in frontend/app/(auth)/signup/page.tsx with email and password form
- [x] T024 [P] [US1] Create login page in frontend/app/(auth)/login/page.tsx with email and password form
- [x] T025 [P] [US1] Create auth context/provider in frontend/lib/auth-context.tsx for session management
- [x] T026 [US1] Implement protected route middleware in frontend/middleware.ts to redirect unauthenticated users
- [x] T027 [US1] Create dashboard layout in frontend/app/(dashboard)/layout.tsx with signout button
- [x] T028 [US1] Add error handling for invalid credentials in login page
- [x] T029 [US1] Add success feedback and redirect after signup in signup page

**Checkpoint**: At this point, User Story 1 should be fully functional - users can signup, signin, signout, and access protected pages

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P2)

**Goal**: Enable authenticated users to create tasks and view their own task list

**Independent Test**: Sign in, create multiple tasks, verify they appear in the list and only show user's own tasks

### Implementation for User Story 2

- [x] T030 [US2] Create Task model in backend/app/models/task.py with id, user_id (FK), title, description, completed, created_at, updated_at fields
- [x] T031 [US2] Create task router in backend/app/routers/tasks.py with create task endpoint (POST /api/tasks)
- [x] T032 [US2] Implement list tasks endpoint in backend/app/routers/tasks.py (GET /api/tasks) filtered by authenticated user
- [x] T033 [US2] Register task router in backend/app/main.py
- [x] T034 [US2] Add title validation (required, max 200 chars) in create task endpoint
- [x] T035 [US2] Add description validation (optional, max 2000 chars) in create task endpoint
- [x] T036 [US2] Ensure tasks are sorted by created_at DESC in list endpoint
- [x] T037 [P] [US2] Create dashboard page in frontend/app/(dashboard)/page.tsx with task list display
- [x] T038 [P] [US2] Create TaskList component in frontend/components/TaskList.tsx to display tasks
- [x] T039 [P] [US2] Create CreateTaskForm component in frontend/components/CreateTaskForm.tsx with title and description inputs
- [x] T040 [US2] Integrate create task API call in CreateTaskForm component
- [x] T041 [US2] Integrate list tasks API call in dashboard page
- [x] T042 [US2] Add loading states for task list fetching
- [x] T043 [US2] Add empty state message when user has no tasks
- [x] T044 [US2] Add validation error display for empty title in CreateTaskForm

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can create and view their tasks

---

## Phase 5: User Story 3 - Update Tasks (Priority: P3)

**Goal**: Enable authenticated users to edit task title and description

**Independent Test**: Create a task, edit its title and description, verify changes persist after page refresh

### Implementation for User Story 3

- [x] T045 [US3] Implement update task endpoint in backend/app/routers/tasks.py (PUT /api/tasks/{task_id})
- [x] T046 [US3] Add authorization check in update endpoint to verify task belongs to authenticated user (return 403 if not)
- [x] T047 [US3] Add validation for title (required, max 200 chars) and description (optional, max 2000 chars) in update endpoint
- [x] T048 [US3] Update updated_at timestamp in update endpoint
- [x] T049 [P] [US3] Create EditTaskModal component in frontend/components/EditTaskModal.tsx with title and description inputs
- [x] T050 [US3] Add edit button to TaskList component that opens EditTaskModal
- [x] T051 [US3] Integrate update task API call in EditTaskModal component
- [x] T052 [US3] Add validation error display in EditTaskModal
- [x] T053 [US3] Refresh task list after successful update

**Checkpoint**: All user stories 1-3 should now be independently functional - users can create, view, and edit tasks

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable authenticated users to permanently remove tasks

**Independent Test**: Create a task, delete it, verify it no longer appears in the list after page refresh

### Implementation for User Story 4

- [x] T054 [US4] Implement delete task endpoint in backend/app/routers/tasks.py (DELETE /api/tasks/{task_id})
- [x] T055 [US4] Add authorization check in delete endpoint to verify task belongs to authenticated user (return 403 if not)
- [x] T056 [US4] Return 204 No Content on successful deletion
- [x] T057 [P] [US4] Add delete button to TaskList component with confirmation dialog
- [x] T058 [US4] Integrate delete task API call in TaskList component
- [x] T059 [US4] Remove deleted task from UI immediately after successful deletion
- [x] T060 [US4] Add success feedback message after deletion

**Checkpoint**: All user stories 1-4 should now be independently functional - users can create, view, edit, and delete tasks

---

## Phase 7: User Story 5 - Mark Tasks Complete (Priority: P5)

**Goal**: Enable authenticated users to mark tasks as complete or incomplete

**Independent Test**: Create a task, mark it complete, mark it incomplete, verify status changes persist after page refresh

### Implementation for User Story 5

- [x] T061 [US5] Add completed status toggle to update task endpoint in backend/app/routers/tasks.py (PATCH /api/tasks/{task_id}/status)
- [x] T062 [US5] Add authorization check in status endpoint to verify task belongs to authenticated user (return 403 if not)
- [x] T063 [P] [US5] Add checkbox to TaskList component for marking tasks complete/incomplete
- [x] T064 [US5] Integrate status update API call in TaskList component
- [x] T065 [US5] Add visual distinction for completed tasks (strikethrough, different color)
- [x] T066 [US5] Update task status in UI immediately after successful API call

**Checkpoint**: All user stories 1-5 should now be independently functional - full CRUD + status management complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T067 [P] Add comprehensive error handling for network failures across all API calls
- [x] T068 [P] Add loading spinners for all async operations (signup, signin, create, update, delete)
- [x] T069 [P] Validate responsive design on mobile (320px), tablet (768px), and desktop (1440px) breakpoints
- [x] T070 [P] Add proper HTTP status codes for all error scenarios (400, 401, 403, 404, 500)
- [x] T071 [P] Add request/response logging in backend for debugging
- [x] T072 [P] Implement proper CORS configuration for production deployment
- [x] T073 [P] Add input sanitization to prevent XSS attacks
- [x] T074 [P] Verify JWT token expiration is enforced (401 on expired tokens)
- [x] T075 [P] Add database connection pooling configuration for Neon
- [x] T076 [P] Create README.md with setup instructions and environment variable documentation
- [x] T077 Verify all acceptance scenarios from spec.md are satisfied
- [x] T078 Verify all functional requirements (FR-001 through FR-033) are implemented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires US1 for authentication but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires US2 for tasks to exist but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Requires US2 for tasks to exist but independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Requires US2 for tasks to exist but independently testable

### Within Each User Story

- Backend endpoints before frontend integration
- Models before routers
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004, T005, T006)
- All Foundational tasks marked [P] can run in parallel within Phase 2 (T010, T011, T012, T015, T016)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each user story, tasks marked [P] can run in parallel
- All Polish tasks marked [P] can run in parallel (T067-T076)

---

## Parallel Example: User Story 1

```bash
# Launch backend auth endpoints together:
Task T017: "Create auth router with signup endpoint"
Task T018: "Implement signin endpoint"
Task T019: "Implement signout endpoint"

# Launch frontend auth pages together:
Task T023: "Create signup page"
Task T024: "Create login page"
Task T025: "Create auth context/provider"
```

---

## Parallel Example: User Story 2

```bash
# Launch frontend components together:
Task T037: "Create dashboard page"
Task T038: "Create TaskList component"
Task T039: "Create CreateTaskForm component"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T016) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T017-T029)
4. **STOP and VALIDATE**: Test User Story 1 independently - users can signup, signin, signout
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T016)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP - Authentication working!)
3. Add User Story 2 → Test independently → Deploy/Demo (Can create and view tasks!)
4. Add User Story 3 → Test independently → Deploy/Demo (Can edit tasks!)
5. Add User Story 4 → Test independently → Deploy/Demo (Can delete tasks!)
6. Add User Story 5 → Test independently → Deploy/Demo (Can mark tasks complete!)
7. Add Polish → Final validation → Production ready!
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T016)
2. Once Foundational is done:
   - Developer A: User Story 1 (T017-T029)
   - Developer B: User Story 2 (T030-T044) - can start in parallel
   - Developer C: User Story 3 (T045-T053) - can start in parallel
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All tasks follow constitution requirements: spec-driven, security-first, JWT authentication, user data isolation
- Backend uses FastAPI + SQLModel, Frontend uses Next.js 16+ App Router, Database is Neon Serverless PostgreSQL
- Better Auth handles JWT token generation, backend validates tokens on every protected endpoint
