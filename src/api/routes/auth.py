from fastapi import APIRouter, HTTPException
from otf_api import Otf
from ..models.schemas import LoginRequest, TokenResponse
from ..core.auth import create_access_token
from ..core.config import settings
from ..core.logging import logger

router = APIRouter()  # Remove the prefix here

# Add both endpoint paths
@router.post("/api/login")  # Original path
@router.post("/api/auth/login")  # New path
async def login(request: LoginRequest):
    otf = None
    try:
        logger.info(f"Login attempt for email: {request.email}")
        otf = Otf(request.email, request.password)
        
        # Verify credentials by attempting to get workout data
        await otf.get_performance_summaries(limit=1)
        
        token_data = {
            "sub": request.email,
            "credentials": {
                "email": request.email,
                "password": request.password
            }
        }
        
        return TokenResponse(
            access_token=create_access_token(token_data),
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        if otf and otf.session:
            await otf.session.close()