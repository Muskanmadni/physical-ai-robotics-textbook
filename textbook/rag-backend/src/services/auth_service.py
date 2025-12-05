from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.models.user import User

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT - in production, set this in environment variables
SECRET_KEY = "your-secret-key-here"  # Should come from environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a hash for a plaintext password."""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Authenticate a user by verifying username and password.
    In a real implementation, this would query the database.
    For now, returning a mock user.
    """
    # In a real implementation, this would be:
    # user = get_user_from_db(username)
    # if user and verify_password(password, user.hashed_password):
    #     return user
    # return None
    
    # Mock implementation
    if username == "test@example.com" and password == "testpassword":
        return User(
            id="mock-user-id",
            email=username,
            name="Test User",
            preferences={},
            createdAt=datetime.now(),
            updatedAt=datetime.now(),
            authProvider="local",
            profilePicture=""
        )
    return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt