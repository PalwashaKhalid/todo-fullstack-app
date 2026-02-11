# Todo Full-Stack Web Application

A secure, multi-user todo application built with FastAPI backend, Next.js frontend, and Neon PostgreSQL database. Features JWT authentication, complete CRUD operations, and responsive design.

## Features

- **User Authentication**: Secure signup/signin with JWT tokens
- **Task Management**: Create, read, update, delete tasks
- **Task Status**: Mark tasks as complete/incomplete
- **Data Isolation**: Users can only access their own tasks
- **Responsive Design**: Works on mobile and desktop devices
- **Real-time Updates**: Immediate UI feedback for all operations

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLModel**: Type-safe ORM for database operations
- **PostgreSQL**: Neon Serverless database
- **JWT**: Stateless authentication with python-jose
- **Bcrypt**: Secure password hashing via passlib

### Frontend
- **Next.js 15+**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Better Auth**: Authentication library with JWT support

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Neon PostgreSQL database account
- Git

## Project Structure

```
Phase-II/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── config.py       # Settings management
│   │   ├── database.py     # Database connection
│   │   ├── models/         # SQLModel schemas
│   │   ├── routers/        # API endpoints
│   │   └── auth/           # Authentication utilities
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
│
├── frontend/               # Next.js application
│   ├── app/                # App Router pages
│   ├── components/         # React components
│   ├── lib/                # Utilities
│   ├── package.json        # Node dependencies
│   └── .env.example        # Environment template
│
└── specs/                  # Feature specifications
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Phase-II
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and configure the following:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host.region.aws.neon.tech/dbname?sslmode=require

# JWT Authentication (generate a secure random string)
JWT_SECRET_KEY=your-secret-key-min-32-chars-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# Better Auth Integration (must match frontend)
BETTER_AUTH_SECRET=shared-secret-with-frontend-min-32-chars

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Important**:
- Get your Neon database URL from [Neon Console](https://console.neon.tech)
- Generate secure random strings for JWT_SECRET_KEY and BETTER_AUTH_SECRET
- Use the same BETTER_AUTH_SECRET in both backend and frontend

#### Run Database Migrations

The application will automatically create database tables on startup.

#### Start Backend Server

```bash
# From backend/ directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

```bash
cp .env.example .env.local
```

Edit `.env.local` and configure:

```bash
# Better Auth Configuration (must match backend)
BETTER_AUTH_SECRET=shared-secret-with-backend-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Database (for Better Auth - same as backend)
DATABASE_URL=postgresql://user:password@host.region.aws.neon.tech/dbname?sslmode=require
```

#### Start Frontend Server

```bash
# From frontend/ directory
npm run dev
```

Frontend will be available at: http://localhost:3000

## Usage

### 1. Create an Account

1. Navigate to http://localhost:3000
2. Click "Sign up"
3. Enter email and password (minimum 8 characters)
4. Click "Sign up" button

### 2. Sign In

1. Navigate to http://localhost:3000/login
2. Enter your email and password
3. Click "Sign in" button

### 3. Manage Tasks

Once signed in, you can:

- **Create Task**: Fill in title and optional description, click "Create Task"
- **View Tasks**: All your tasks are displayed in the dashboard
- **Mark Complete**: Click the checkbox to toggle task completion status
- **Edit Task**: Click "Edit" button, modify title/description, click "Save Changes"
- **Delete Task**: Click "Delete" button, confirm deletion

### 4. Sign Out

Click "Sign out" button in the navigation bar.

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in and receive JWT token
- `POST /api/auth/signout` - Sign out (client-side token removal)

### Tasks (Protected - Requires JWT)

- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{task_id}` - Update task title and description
- `DELETE /api/tasks/{task_id}` - Delete task
- `PATCH /api/tasks/{task_id}/status` - Toggle task completion status

## Security Features

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Authentication**: Stateless token-based auth
- **Data Isolation**: Users can only access their own tasks
- **Authorization Checks**: All operations verify task ownership
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection Prevention**: Parameterized queries via SQLModel
- **XSS Prevention**: React auto-escaping + input sanitization
- **CORS Configuration**: Explicit allowed origins

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Troubleshooting

### Backend Issues

**Database connection fails**
- Verify DATABASE_URL is correct
- Check Neon database is running
- Ensure SSL mode is enabled: `?sslmode=require`

**JWT token validation fails**
- Verify JWT_SECRET_KEY matches between backend and frontend
- Check token is being sent in Authorization header
- Ensure token hasn't expired

**CORS errors**
- Add frontend URL to CORS_ORIGINS in backend .env
- Verify CORS middleware is configured in main.py

### Frontend Issues

**API requests fail**
- Verify NEXT_PUBLIC_API_URL points to backend
- Check backend server is running
- Verify JWT token is stored in localStorage

**Authentication doesn't work**
- Verify BETTER_AUTH_SECRET matches backend
- Check DATABASE_URL is correct
- Clear browser localStorage and try again

**Tasks don't load**
- Check browser console for errors
- Verify JWT token is valid
- Check backend logs for errors

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | Neon PostgreSQL connection string | postgresql://user:pass@host/db |
| JWT_SECRET_KEY | Secret key for JWT signing | min-32-chars-random-string |
| JWT_ALGORITHM | JWT algorithm | HS256 |
| JWT_EXPIRATION_MINUTES | Token expiration time | 30 |
| BETTER_AUTH_SECRET | Shared secret with frontend | min-32-chars-random-string |
| API_HOST | Backend host | 0.0.0.0 |
| API_PORT | Backend port | 8000 |
| CORS_ORIGINS | Allowed CORS origins | http://localhost:3000 |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| BETTER_AUTH_SECRET | Shared secret with backend | min-32-chars-random-string |
| BETTER_AUTH_URL | Frontend URL | http://localhost:3000 |
| NEXT_PUBLIC_API_URL | Backend API URL | http://localhost:8000 |
| DATABASE_URL | Neon PostgreSQL connection string | postgresql://user:pass@host/db |

## Development Workflow

This project follows the **Agentic Dev Stack** workflow:

1. **Spec**: Feature specification in `specs/001-todo-web-app/spec.md`
2. **Plan**: Architecture plan in `specs/001-todo-web-app/plan.md`
3. **Tasks**: Task breakdown in `specs/001-todo-web-app/tasks.md`
4. **Implement**: Code generation via Claude Code

All code is generated through this workflow - no manual coding.

## Contributing

This project was built for Hackathon Phase-II following spec-driven development principles. All changes should:

1. Start with a specification
2. Create an architectural plan
3. Break down into testable tasks
4. Implement via Claude Code

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at http://localhost:8000/docs
3. Check browser console and backend logs for errors

## Acknowledgments

- Built with Claude Code and Spec-Kit Plus
- Uses Neon Serverless PostgreSQL
- Follows FastAPI and Next.js best practices
