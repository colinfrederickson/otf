from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from otf_api import Otf
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
import logging
import os
import asyncio

# Basic setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# FastAPI app setup
app = FastAPI(
    title="OrangeTheory Fitness API",
    description="API for accessing OrangeTheory Fitness workout data and member information.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }

class MemberDetail(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr

# Helper functions
async def get_otf_client(credentials):
    """Create and return an OTF client"""
    return Otf(credentials["email"], credentials["password"])

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        credentials = payload.get("credentials")
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired or is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

# API endpoints
@app.post("/api/login")
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
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()

@app.get("/api/total-classes")
async def get_total_classes(token: str = Depends(oauth2_scheme)):
    """Get total class counts and workout history"""
    otf = None
    try:
        credentials = decode_token(token)
        otf = await get_otf_client(credentials)
        
        # Get data in parallel
        workouts, total_classes = await asyncio.gather(
            otf.get_performance_summaries(limit=None),
            otf.get_total_classes()
        )
        
        return {
            "performance_data": {
                "retrieved_workouts": len(workouts.summaries)
            },
            "total_classes": {
                "in_studio": total_classes.total_in_studio_classes_attended,
                "ot_live": total_classes.total_otlive_classes_attended,
                "total": total_classes.total_in_studio_classes_attended + total_classes.total_otlive_classes_attended
            },
            "date_range": {
                "first_class": workouts.summaries[0].otf_class.starts_at_local,
                "last_class": workouts.summaries[-1].otf_class.starts_at_local
            } if workouts.summaries else None,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()

@app.get("/api/member-detail")
async def get_member_detail(token: str = Depends(oauth2_scheme)):
    """Get member profile information"""
    otf = None
    try:
        credentials = decode_token(token)
        otf = await get_otf_client(credentials)
        member_detail = await otf.get_member_detail()
        
        return {
            "status": "success",
            "data": {
                "first_name": member_detail.first_name,
                "last_name": member_detail.last_name,
                "user_name": member_detail.user_name,
                "email": member_detail.email,
            }
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if otf and hasattr(otf, 'session') and otf.session:
            await otf.session.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)