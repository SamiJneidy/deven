import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ..config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/authorize")
pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def create_access_token(payload: dict, expires_delta: timedelta = timedelta(minutes=settings.access_token_expire_minutes)) -> str:
    """Creates access token and returns it as a string"""
    payload["iat"] = datetime.now(tz=timezone.utc)
    payload["exp"] = datetime.now(tz=timezone.utc) + expires_delta
    return jwt.encode(payload, settings.secret_key, settings.algorithm)

    
async def decode_token(token: str) -> dict | None:
    """Decodes a token and returns its payload as a dictionary. Returns None when the token is invalid"""
    try:
        payload: dict = jwt.decode(jwt=token, key=settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.InvalidTokenError:
        return None
    

async def validate_access_token(token: str) -> bool:
    """Returns True if the token is valid, False otherwise"""
    return decode_token(token) is not None
