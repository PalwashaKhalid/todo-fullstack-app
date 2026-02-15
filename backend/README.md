---
title: Todo App Backend API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Todo API Backend

Secure multi-user task management API built with FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Features

- ✅ RESTful API with JWT authentication
- ✅ Per-user data isolation
- ✅ CRUD operations for tasks
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ PostgreSQL database with connection pooling
- ✅ Input validation with Pydantic
- ✅ CORS support for frontend integration

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **ORM**: SQLModel 0.0.14
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT (python-jose)
- **Server**: Uvicorn with auto-reload

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
BETTER_AUTH_SECRET=shared-secret-with-frontend
API_HOST=0.0.0.0
API_PORT=8001
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Start the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The API will be available at:
- **API**: http://localhost:8001
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## API Endpoints

### Health Check

```
GET /              - Root health check
GET /health        - Detailed health status
```

### Tasks (Requires JWT Authentication)

All task endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.

```
POST   /api/tasks/              - Create new task
GET    /api/tasks/              - List user's tasks
GET    /api/tasks/?completed=true  - Filter by completion status
GET    /api/tasks/{id}          - Get specific task
PUT    /api/tasks/{id}          - Update task title/description
PATCH  /api/tasks/{id}/status   - Update completion status
DELETE /api/tasks/{id}          - Delete task
```

## Request/Response Examples

### Create Task

**Request:**
```bash
curl -X POST http://localhost:8001/api/tasks/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API docs"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "completed": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### List Tasks

**Request:**
```bash
curl -X GET http://localhost:8001/api/tasks/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "title": "Complete project documentation",
      "description": "Write comprehensive API docs",
      "completed": false,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "message": "Retrieved 1 task(s)"
}
```

### Update Task Status

**Request:**
```bash
curl -X PATCH http://localhost:8001/api/tasks/1/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API docs",
  "completed": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:01Z"
}
```

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. The JWT token should be obtained from the frontend authentication system (Better Auth) and included in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

### JWT Token Format

The JWT token must contain:
- `sub`: User ID (string)
- `email`: User email (string)
- `exp`: Expiration timestamp

### Security Features

- All task endpoints require valid JWT authentication
- Users can only access their own tasks (enforced at database query level)
- Cross-user access attempts return 403 Forbidden
- Invalid/expired tokens return 401 Unauthorized

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_id_created_at ON tasks(user_id, created_at);
```

## Error Handling

The API returns standard HTTP status codes:

- **200 OK**: Successful GET/PUT/PATCH request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Valid token but insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server-side error

Error responses include a detail message:

```json
{
  "detail": "Task with ID 999 not found"
}
```

## Development

### Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py         # Task endpoints
│   └── auth/
│       ├── __init__.py
│       ├── jwt.py           # JWT verification
│       └── dependencies.py  # Auth dependencies
├── tests/
│   ├── __init__.py
│   └── test_tasks.py        # API tests
├── .env                     # Environment variables
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
└── README.md
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

The codebase follows:
- PEP 8 style guidelines
- Type hints for all functions
- Comprehensive docstrings
- Input validation with Pydantic
- Secure coding practices (no SQL injection, proper auth)

## Deployment

### Environment Variables

Ensure all required environment variables are set:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing (min 32 characters)
- `BETTER_AUTH_SECRET`: Shared secret with frontend
- `API_PORT`: Port to run the server (default: 8001)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Production Considerations

1. **Database**: Use Neon's production branch with appropriate compute settings
2. **Secrets**: Use environment variables, never commit secrets to git
3. **CORS**: Restrict `CORS_ORIGINS` to your production domain
4. **SSL**: Ensure `sslmode=require` in `DATABASE_URL`
5. **Monitoring**: Set up logging and error tracking
6. **Rate Limiting**: Consider adding rate limiting middleware

## License

This project is part of the Hackathon-II Phase-II implementation.
