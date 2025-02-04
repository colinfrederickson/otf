from fastapi import APIRouter, HTTPException, status
from api.core.config import logger
from api.core.auth import create_access_token
from api.models.schemas import LoginRequest
from otf_api import Otf

router = APIRouter()

@router.post("/login")
async def login(request: LoginRequest):
    """Authenticate user and return access token"""
    otf = None
    try:
        logger.info(f"Login attempt for email: {request.email}")
        otf = Otf(request.email, request.password)
        
        # Verify credentials
        await otf.get_performance_summaries(limit=1)
        
        token_data = {
            "sub": request.email,
            "credentials": {
                "email": request.email,
                "password": request.password
            }
        }
        
        return {
            "access_token": create_access_token(token_data),
            "token_type": "bearer",
            "expires_in": 60 * 24 * 60
        }
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()