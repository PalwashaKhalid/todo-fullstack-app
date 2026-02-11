# Quickstart Guide: Todo Full-Stack Web Application

**Feature**: 001-todo-web-app
**Date**: 2026-02-06
**Phase**: Phase 1 - Setup Instructions

## Overview

This guide provides step-by-step instructions to set up and run the Todo Full-Stack Web Application locally. The application consists of a FastAPI backend, Next.js frontend, and Neon PostgreSQL database.

## Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **npm**: 9 or higher (comes with Node.js)
- **Git**: Latest version
- **PostgreSQL Client** (optional, for database inspection): `psql`

### Required Accounts

- **Neon Account**: Sign up at https://neon.tech for serverless PostgreSQL database
- **GitHub Account** (optional): For version control and collaboration

### System Requirements

- **OS**: Linux, macOS, or Windows (with WSL2 recommended)
- **RAM**: Minimum 4GB, recommended 8GB
- **Disk Space**: Minimum 2GB free space

---

## Project Structure

```
Phase-II/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── specs/            # Feature specifications
└── .gitignore        # Git ignore patterns
```

---

## Setup Instructions

### Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd Phase-II

# Checkout the feature branch
git checkout 001-todo-web-app
```

### Step 2: Set Up Neon Database

1. **Create Neon Account**:
   - Visit https://neon.tech
   - Sign up for a free account
   - Create a new project named "todo-app"

2. **Get Database Connection String**:
   - In Neon dashboard, navigate to your project
   - Copy the connection string (format: `postgresql://user:password@host/dbname`)
   - Save this for environment configuration

3. **Create Database Tables** (will be done automatically by backend on first run)

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Edit .env file with your configuration
nano .env  # or use your preferred editor
```

**Backend .env Configuration**:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/dbname
NEON_DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-min-32-chars-generate-with-openssl
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Better Auth Integration
BETTER_AUTH_SECRET=shared-secret-with-frontend-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Generate Secure Secrets**:

```bash
# Generate JWT_SECRET_KEY
openssl rand -hex 32

# Generate BETTER_AUTH_SECRET
openssl rand -hex 32
```

**Initialize Database**:

```bash
# Run database migrations (creates tables)
python -m app.database

# Or start the server (will auto-create tables)
uvicorn app.main:app --reload
```

### Step 4: Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create .env.local file from template
cp .env.example .env.local

# Edit .env.local file with your configuration
nano .env.local  # or use your preferred editor
```

**Frontend .env.local Configuration**:

```bash
# Better Auth
BETTER_AUTH_SECRET=same-secret-as-backend-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database (for Better Auth)
DATABASE_URL=postgresql://user:password@host/dbname
```

**Important**: The `BETTER_AUTH_SECRET` must match between frontend and backend.

### Step 5: Verify Setup

**Check Backend**:

```bash
# From backend directory
cd backend
source venv/bin/activate  # if not already activated
uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Check Frontend**:

```bash
# From frontend directory (in a new terminal)
cd frontend
npm run dev

# You should see:
# ▲ Next.js 16.x.x
# - Local:        http://localhost:3000
# - Ready in Xs
```

---

## Running the Application

### Development Mode

**Terminal 1 - Backend**:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:

```bash
cd frontend
npm run dev
```

**Access the Application**:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs (Swagger UI)
- Alternative API Docs: http://localhost:8000/redoc (ReDoc)

### Production Mode

**Backend**:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend**:

```bash
cd frontend
npm run build
npm start
```

---

## Testing the Application

### Manual Testing Flow

1. **Open Frontend**: Navigate to http://localhost:3000

2. **Create Account**:
   - Click "Sign Up"
   - Enter email and password (min 8 characters)
   - Submit form
   - You should be redirected to dashboard

3. **Create Task**:
   - Enter task title in the form
   - Optionally add description
   - Click "Create Task"
   - Task should appear in the list

4. **Update Task**:
   - Click "Edit" on a task
   - Modify title or description
   - Save changes
   - Changes should persist

5. **Mark Complete**:
   - Click checkbox on a task
   - Task should be visually marked as complete
   - Status should persist on page refresh

6. **Delete Task**:
   - Click "Delete" on a task
   - Confirm deletion
   - Task should be removed from list

7. **Sign Out**:
   - Click "Sign Out"
   - You should be redirected to login page
   - Protected pages should be inaccessible

8. **Sign In**:
   - Enter your email and password
   - Submit form
   - You should see your tasks again

### API Testing with curl

**Signup**:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Signin**:

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

**Create Task** (replace TOKEN with JWT from signin):

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{"title":"Test task","description":"Test description"}'
```

**List Tasks**:

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer TOKEN"
```

### Automated Testing

**Backend Tests**:

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

**Frontend Tests**:

```bash
cd frontend
npm test
```

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Ensure you're in the backend directory
cd backend
# Ensure virtual environment is activated
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

**Issue**: `Database connection failed`

**Solution**:
- Verify `DATABASE_URL` in `.env` is correct
- Check Neon database is running (visit Neon dashboard)
- Ensure SSL mode is enabled: `?sslmode=require`
- Test connection: `psql $DATABASE_URL`

**Issue**: `CORS error in browser`

**Solution**:
- Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:3000`
- Restart backend server after changing `.env`
- Clear browser cache

### Frontend Issues

**Issue**: `Module not found` errors

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue**: `API calls return 401 Unauthorized`

**Solution**:
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check JWT token is being sent in Authorization header
- Verify backend is running on correct port (8000)
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`

**Issue**: `Better Auth configuration error`

**Solution**:
- Verify `DATABASE_URL` in frontend `.env.local` is correct
- Ensure Better Auth tables are created in database
- Restart frontend dev server after changing `.env.local`

### Database Issues

**Issue**: `relation "users" does not exist`

**Solution**:
```bash
# Run database initialization
cd backend
source venv/bin/activate
python -m app.database
```

**Issue**: `Connection pool exhausted`

**Solution**:
- Check for connection leaks in code
- Verify connection pooling is configured
- Restart backend server
- Check Neon dashboard for connection limits

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| DATABASE_URL | Yes | Neon PostgreSQL connection string | `postgresql://user:pass@host/db` |
| NEON_DATABASE_URL | Yes | Same as DATABASE_URL with SSL | `postgresql://user:pass@host/db?sslmode=require` |
| JWT_SECRET_KEY | Yes | Secret for JWT signing (min 32 chars) | Generated with `openssl rand -hex 32` |
| JWT_ALGORITHM | Yes | JWT signing algorithm | `HS256` |
| JWT_EXPIRATION_MINUTES | Yes | JWT token expiration time | `30` |
| BETTER_AUTH_SECRET | Yes | Shared secret with frontend (min 32 chars) | Generated with `openssl rand -hex 32` |
| BETTER_AUTH_URL | Yes | Frontend URL | `http://localhost:3000` |
| API_HOST | Yes | Backend host | `0.0.0.0` |
| API_PORT | Yes | Backend port | `8000` |
| CORS_ORIGINS | Yes | Allowed CORS origins (comma-separated) | `http://localhost:3000` |

### Frontend (.env.local)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| BETTER_AUTH_SECRET | Yes | Shared secret with backend (must match) | Same as backend |
| BETTER_AUTH_URL | Yes | Frontend URL | `http://localhost:3000` |
| NEXT_PUBLIC_API_URL | Yes | Backend API URL | `http://localhost:8000` |
| DATABASE_URL | Yes | Neon PostgreSQL connection string | Same as backend |

---

## Development Workflow

### Making Changes

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**: Edit code in backend/ or frontend/

3. **Test Changes**: Run manual and automated tests

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. **Push Changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Hot Reload

- **Backend**: `--reload` flag enables auto-restart on code changes
- **Frontend**: Next.js dev server auto-reloads on file changes

### Debugging

**Backend**:
- Add `import pdb; pdb.set_trace()` for breakpoints
- Check logs in terminal running uvicorn
- Use FastAPI's `/docs` endpoint to test API manually

**Frontend**:
- Use browser DevTools (F12)
- Check Console for errors
- Use Network tab to inspect API calls
- Use React DevTools extension

---

## Security Checklist

Before deploying to production:

- [ ] Change all default secrets (JWT_SECRET_KEY, BETTER_AUTH_SECRET)
- [ ] Use strong, randomly generated secrets (min 32 characters)
- [ ] Never commit `.env` or `.env.local` files to git
- [ ] Enable HTTPS in production
- [ ] Set `sslmode=require` for database connections
- [ ] Configure proper CORS origins (no wildcards)
- [ ] Set appropriate JWT expiration time
- [ ] Enable rate limiting on API endpoints
- [ ] Set up database backups
- [ ] Configure logging and monitoring

---

## Next Steps

After successful setup:

1. **Review Specification**: Read `specs/001-todo-web-app/spec.md`
2. **Review Implementation Plan**: Read `specs/001-todo-web-app/plan.md`
3. **Review Data Model**: Read `specs/001-todo-web-app/data-model.md`
4. **Review API Contracts**: Check `specs/001-todo-web-app/contracts/`
5. **Start Implementation**: Run `/sp.implement` to begin code generation

---

## Support

For issues or questions:

- Check troubleshooting section above
- Review error messages in terminal
- Check API documentation at http://localhost:8000/docs
- Review spec and plan documents in `specs/001-todo-web-app/`

---

## Summary

**Setup Time**: ~15-20 minutes
**Prerequisites**: Python 3.11+, Node.js 18+, Neon account
**Ports Used**: 3000 (frontend), 8000 (backend)
**Database**: Neon Serverless PostgreSQL

**Quick Start Commands**:

```bash
# Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend && npm run dev

# Access: http://localhost:3000
```
