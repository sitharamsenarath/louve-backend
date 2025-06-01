from passlib.context import CryptContext

# Create a CryptContext instance with bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against the hashed password"""
    return pwd_context.verify(plain_password, hashed_password)
