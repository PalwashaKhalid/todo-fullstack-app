from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.database import get_db
from src.models.user import User, UserCreate, UserLogin, UserResponse
from src.auth.password import hash_password, verify_password
from src.auth.jwt import create_access_token
import re

router = APIRouter(prefix="/api/auth", tags=["authentication"])


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account

    Args:
        user_data: User registration data (email, password)
        db: Database session

    Returns:
        JWT token and user information

    Raises:
        HTTPException: 400 if email is invalid or already exists
    """
    # Validate email format
    if not validate_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password strength (minimum 8 characters)
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    # Check if email already exists
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(new_user.id), "email": new_user.email}
    )

    return {
        "success": True,
        "data": {
            "token": access_token,
            "user": UserResponse(
                id=new_user.id,
                email=new_user.email,
                created_at=new_user.created_at
            )
        },
        "message": "Account created successfully"
    }


@router.post("/signin", response_model=dict)
async def signin(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token

    Args:
        credentials: User login credentials (email, password)
        db: Database session

    Returns:
        JWT token and user information

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Find user by email
    user = db.exec(select(User).where(User.email == credentials.email)).first()

    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}
    )

    return {
        "success": True,
        "data": {
            "token": access_token,
            "user": UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at
            )
        },
        "message": "Signed in successfully"
    }


@router.post("/signout", response_model=dict)
async def signout():
    """
    Sign out user (client-side token removal)

    Returns:
        Success message
    """
    return {
        "success": True,
        "message": "Signed out successfully"
    }
