from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.utils.utils import Utils

# Use environment variables for production!
env_variables = Utils.load_dotenv_variables()
SECRET_KEY = env_variables[-1]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    """
    Create a JWT token containing the data dictionary.
    Automatically adds expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    """
    Verify a JWT token. Returns the payload if valid, else None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
