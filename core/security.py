from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from settings import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Converts a plaintext password into a secure hashed representation
    using the configured password context. The hash can be safely stored
    in a database and later verified without exposing the original password.
    Args:
        password (str): The plaintext password to hash.
    Returns:
        str: The hashed password string.
    """

    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain text password against a hashed password.
    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    *,
    user_id: int,
    session_id: int,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Creates an access token for a user session.
    Args:
        user_id (int): The unique identifier of the user.
        session_id (int): The unique identifier of the session.
        expires_delta (timedelta | None, optional): The duration for which the token is valid. 
            If None, the token will expire after a default duration defined by 
            ACCESS_TOKEN_EXPIRE_MINUTES.
    Returns:
        str: The encoded JWT access token.
    Raises:
        Exception: If there is an error during token creation.
    Usage:
        token = create_access_token(user_id=123, session_id=456)
    """
    
    # expire = datetime.utcnow() + (
    #     expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    # )
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": str(user_id),
        "sid": session_id,
        "exp": expire,
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Decode an access token and return the payload as a dictionary.
    Args:
        token (str): The JWT access token to decode.
    Returns:
        dict: The decoded payload if the token is valid, otherwise an empty dictionary.
    Raises:
        JWTError: If the token is invalid or cannot be decoded.
    """

    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return {}
