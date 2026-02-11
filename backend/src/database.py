from sqlmodel import SQLModel, create_engine, Session
from src.config import settings

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
)


def create_db_and_tables():
    """Create all database tables from SQLModel definitions"""
    SQLModel.metadata.create_all(engine)


def get_db():
    """Dependency for getting database session"""
    with Session(engine) as session:
        yield session
