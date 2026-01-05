from passlib.context import CryptContext


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
