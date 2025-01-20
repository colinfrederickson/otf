import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel
from src.analyzer import OTFAnalytics
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configurations
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LoginRequest(BaseModel):
    email: str
    password: str

def create_access_token(data: dict):
    """Create a new access token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        credentials = payload.get("credentials")
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid token format")
        return credentials
    except JWTError:
        raise HTTPException(status_code=401, detail="Token has expired or is invalid")

@app.post("/api/login")
async def login(request: LoginRequest):
    analytics = None
    try:
        logger.info(f"Login attempt for email: {request.email}")
        analytics = OTFAnalytics(request.email, request.password)
        
        # Verify credentials by attempting to get workout data
        await analytics.get_workout_data(limit=1)
        
        token_data = {
            "sub": request.email,
            "credentials": {
                "email": request.email,
                "password": request.password
            }
        }
        access_token = create_access_token(token_data)
        
        logger.info(f"Login successful for email: {request.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except Exception as e:
        logger.error(f"Login failed for email {request.email}: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    finally:
        if analytics:
            await analytics.close()

@app.get("/api/total-classes")
async def get_total_classes(token: str = Depends(oauth2_scheme)):
    analytics = None
    try:
        credentials = decode_token(token)
        logger.info(f"Fetching class data for email: {credentials['email']}")
        
        analytics = OTFAnalytics(
            credentials["email"],
            credentials["password"]
        )
        
        # Get both workout summaries and class data
        workouts = await analytics.get_workout_data(limit=None)
        class_data = await analytics.get_class_data()
        
        # Prepare response with combined data
        response = {
            "performance_data": {
                "retrieved_workouts": len(workouts)
            },
            "total_classes": {
                "in_studio": class_data["total_in_studio_classes"],
                "ot_live": class_data["total_otlive_classes"],
                "total": class_data["total_in_studio_classes"] + class_data["total_otlive_classes"]
            },
            "date_range": None,
            "status": "success",
            "message": "Data retrieved successfully"
        }
        
        # Add date range if workouts exist
        if workouts:
            response["date_range"] = {
                "first_class": workouts[0].otf_class.starts_at_local,
                "last_class": workouts[-1].otf_class.starts_at_local
            }
        
        logger.info(f"Successfully retrieved data for {credentials['email']}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving class data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while retrieving class data"
        )
    finally:
        if analytics:
            try:
                await analytics.close()
            except Exception as e:
                logger.error(f"Error closing analytics session: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)