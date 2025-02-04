from pydantic import BaseModel, EmailStr
from datetime import datetime

# Auth Models
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

# Member Models
class StudioInfo(BaseModel):
    home_studio_name: str
    total_studios_visited: int
    time_zone: str

class WorkoutStats(BaseModel):
    total_classes_booked: int
    total_classes_attended: int
    total_classes_with_hrm: int
    attendance_rate: float
    hrm_usage_rate: float
    first_class_date: datetime
    last_class_date: datetime

class MemberDetail(BaseModel):
    # Basic Info
    first_name: str
    last_name: str
    email: EmailStr
    
    # Fitness Profile
    max_hr: int
    
    # Stats
    workout_stats: WorkoutStats
    studio_info: StudioInfo

# Response Models
class MemberDetailResponse(BaseModel):
    status: str
    data: MemberDetail