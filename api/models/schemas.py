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

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jane@example.com",
                    "max_hr": 195,
                    "workout_stats": {
                        "total_classes_booked": 10,
                        "total_classes_attended": 9,
                        "total_classes_with_hrm": 8,
                        "attendance_rate": 90.0,
                        "hrm_usage_rate": 88.9,
                        "first_class_date": "2023-01-01T00:00:00",
                        "last_class_date": "2023-06-30T00:00:00"
                    },
                    "studio_info": {
                        "home_studio_name": "Downtown",
                        "total_studios_visited": 3,
                        "time_zone": "UTC"
                    }
                }
            }
        }
