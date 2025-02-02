from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from otf_api import Otf
from .config import settings
from .logging import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        credentials = payload.get("credentials")
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid token format")
        return credentials
    except JWTError:
        raise HTTPException(status_code=401, detail="Token has expired or is invalid")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    return decode_token(token)

async def get_otf_client(credentials: dict) -> Otf:
    """Create and return an OTF client"""
    return Otf(credentials["email"], credentials["password"])