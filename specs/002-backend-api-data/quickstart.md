# Quickstart Guide: Backend API & Data Layer

**Feature**: Backend API & Data Layer (002-backend-api-data)
**Date**: 2026-02-06
**Purpose**: Setup and run instructions for the FastAPI backend with Neon PostgreSQL

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **pip** package manager
- **Neon PostgreSQL database** provisioned (get connection string from Neon console)
- **JWT secret key** shared with Better Auth frontend (minimum 32 characters)
- **Git** for version control

---

## 1. Environment Setup

### Clone Repository (if not already done)

```bash
git clone <repository-url>
cd Phase-II
git checkout 002-backend-api-data
```

### Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Required packages** (requirements.txt):
```
fastapi==0.109.0
sqlmodel==0.0.14
uvicorn[standard]==0.27.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic-settings==2.1.0
psycopg2-binary==2.9.9
```

---

## 2. Environment Configuration

### Create .env File

Create `backend/.env` file with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host.region.aws.neon.tech/dbname?sslmode=require
NEON_DATABASE_URL=postgresql://user:password@host.region.aws.neon.tech/dbname?sslmode=require

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-minimum-32-characters-long
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Better Auth Integration
BETTER_AUTH_SECRET=shared-secret-with-frontend-min-32-chars

# API Configuration
API_HOST=0.0.0.0
API_PORT=8001
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Get Neon Database Connection String

1. Log in to [Neon Console](https://console.neon.tech)
2. Select your project
3. Go to "Connection Details"
4. Copy the connection string (format: `postgresql://user:password@host/dbname`)
5. Add `?sslmode=require` to the end
6. Paste into `DATABASE_URL` in .env file

### Generate JWT Secret

```bash
# Generate secure random secret (32+ characters)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output to `JWT_SECRET_KEY` in .env file.

### Share Secret with Frontend

The `BETTER_AUTH_SECRET` must match the secret used by Better Auth in the frontend. Coordinate with frontend team to use the same secret.

---

## 3. Database Initialization

### Create Database Tables

The application automatically creates tables on startup using SQLModel.

**Manual creation** (if needed):

```python
# Run from backend/ directory
python -c "
from app.database import engine
from app.models.user import User
from app.models.task import Task
from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
print('✓ Database tables created')
"
```

### Verify Tables Created

Connect to your Neon database and verify:

```sql
-- Check tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Should show: users, tasks

-- Check indexes
SELECT indexname FROM pg_indexes
WHERE schemaname = 'public';

-- Should show: idx_users_email, idx_tasks_user_id, idx_tasks_user_created
```

---

## 4. Running the Server

### Start Development Server

```bash
# From backend/ directory with venv activated
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Verify Server Running

Open browser to: http://localhost:8001

**Expected response:**
```json
{
  "success": true,
  "message": "Todo API is running",
  "version": "1.0.0"
}
```

### Access API Documentation

**Swagger UI**: http://localhost:8001/docs
**ReDoc**: http://localhost:8001/redoc

---

## 5. Testing the API

### Health Check

```bash
curl http://localhost:8001/health
```

**Expected response:**
```json
{
  "success": true,
  "status": "healthy"
}
```

### Create Test User (via Auth Service)

First, create a user through the authentication service (Better Auth frontend) or manually:

```bash
# Example: Create user via auth endpoint (if implemented)
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

**Expected response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "test@example.com"
    }
  }
}
```

### Create Task (Authenticated)

```bash
# Save token from signup/signin response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:8001/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Expected response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-06T10:30:00Z",
    "updated_at": "2026-02-06T10:30:00Z"
  },
  "message": "Task created successfully"
}
```

### List Tasks

```bash
curl -X GET http://localhost:8001/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

**Expected response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-02-06T10:30:00Z",
      "updated_at": "2026-02-06T10:30:00Z"
    }
  ]
}
```

### Update Task

```bash
curl -X PUT http://localhost:8001/api/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Buy groceries and cook dinner",
    "description": "Milk, eggs, bread, chicken"
  }'
```

### Toggle Completion Status

```bash
curl -X PATCH http://localhost:8001/api/tasks/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "completed": true
  }'
```

### Delete Task

```bash
curl -X DELETE http://localhost:8001/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected response:** 204 No Content (empty body)

---

## 6. Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

### Run All Tests

```bash
# From backend/ directory
pytest
```

### Run Specific Test File

```bash
pytest tests/test_tasks.py
pytest tests/test_auth.py
pytest tests/test_security.py
```

### Run with Coverage

```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

View coverage report: `open htmlcov/index.html`

---

## 7. Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution**: Ensure you're in the `backend/` directory and virtual environment is activated.

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: "Database connection failed"

**Solution**: Verify DATABASE_URL in .env file:
- Check connection string format
- Ensure `?sslmode=require` is appended
- Verify Neon database is running (check Neon console)
- Test connection: `psql $DATABASE_URL`

### Issue: "Invalid token" errors

**Solution**: Verify JWT configuration:
- Check `JWT_SECRET_KEY` matches between backend and auth service
- Ensure `BETTER_AUTH_SECRET` matches frontend configuration
- Verify token is being sent in `Authorization: Bearer <token>` header
- Check token hasn't expired (default: 24 hours)

### Issue: "CORS errors" in browser

**Solution**: Update CORS_ORIGINS in .env:
```bash
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://yourdomain.com
```

Restart server after changing .env file.

### Issue: Port 8001 already in use

**Solution**: Kill existing process or use different port:

```bash
# Find process using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8002
```

### Issue: "Table already exists" error

**Solution**: SQLModel tries to create tables on startup. If tables exist, this is normal and can be ignored. To recreate tables:

```bash
# Connect to database and drop tables
psql $DATABASE_URL -c "DROP TABLE IF EXISTS tasks CASCADE; DROP TABLE IF EXISTS users CASCADE;"

# Restart server to recreate tables
```

---

## 8. Development Workflow

### Code Changes

1. Make changes to code in `backend/app/`
2. Server auto-reloads (if using `--reload` flag)
3. Test changes via Swagger UI or curl
4. Run tests: `pytest`
5. Commit changes: `git add . && git commit -m "Description"`

### Database Schema Changes

1. Update SQLModel models in `app/models/`
2. Drop and recreate tables (development only):
   ```bash
   psql $DATABASE_URL -c "DROP TABLE IF EXISTS tasks CASCADE;"
   ```
3. Restart server to create new schema
4. For production: Use Alembic migrations (future enhancement)

### Adding New Endpoints

1. Create route handler in `app/routers/`
2. Add authentication dependency: `current_user: dict = Depends(get_current_user)`
3. Filter queries by `current_user["id"]`
4. Update OpenAPI spec in `specs/002-backend-api-data/contracts/openapi.yaml`
5. Add tests in `tests/`

---

## 9. Production Deployment

### Environment Variables

Set production values for:
- `DATABASE_URL`: Production Neon database
- `JWT_SECRET_KEY`: Strong random secret (rotate periodically)
- `BETTER_AUTH_SECRET`: Production secret (shared with frontend)
- `CORS_ORIGINS`: Production frontend URLs only

### Run Production Server

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn (production ASGI server)
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8001 \
  --access-logfile - \
  --error-logfile -
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

Build and run:
```bash
docker build -t task-api .
docker run -p 8001:8001 --env-file .env task-api
```

---

## 10. Next Steps

1. **Integrate with Frontend**: Coordinate with frontend team on API endpoints and JWT token format
2. **Add Tests**: Write comprehensive tests for all endpoints (see `tests/` directory)
3. **Monitor Performance**: Use Neon console to monitor query performance and database usage
4. **Add Logging**: Implement structured logging for production debugging
5. **Set Up CI/CD**: Automate testing and deployment

---

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com
- **Neon Documentation**: https://neon.tech/docs
- **JWT.io**: https://jwt.io (decode and verify JWT tokens)
- **API Documentation**: http://localhost:8001/docs (when server running)

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review API documentation at `/docs` endpoint
3. Check Neon console for database issues
4. Review application logs for error details

**Status**: ✅ Backend ready for development and testing
