"""
FastAPI application entry point.
Configures CORS, registers routers, and handles application lifecycle.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config import settings
from src.database import create_db_and_tables
from src.routers import tasks, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    print("🚀 Starting up...")
    print(f"📊 Creating database tables...")
    create_db_and_tables()
    print(f"✅ Database tables created")
    print(f"🌐 API running on http://{settings.API_HOST}:{settings.API_PORT}")

    yield

    # Shutdown
    print("👋 Shutting down...")


# Initialize FastAPI application
app = FastAPI(
    title="Todo API",
    description="Secure multi-user task management API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(tasks.router)


# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API status check."""
    return {
        "success": True,
        "message": "Todo API is running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "success": True,
        "status": "healthy",
        "message": "API is operational"
    }
