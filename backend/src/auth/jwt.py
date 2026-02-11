from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.config import settings


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token

    Args:
        data: Dictionary containing user data (typically {"sub": user_id, "email": email})

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """
    Decode and validate a JWT access token

    Args:
        token: JWT token string

    Returns:
        Decoded token payload or None if invalid/expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
