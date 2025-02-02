from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class MemberDetailResponse(BaseModel):
    status: str
    data: Dict[str, str]

class DateRange(BaseModel):
    first_class: datetime
    last_class: datetime

class PerformanceData(BaseModel):
    retrieved_workouts: int

class TotalClasses(BaseModel):
    in_studio: int
    ot_live: int
    total: int

class ClassesResponse(BaseModel):
    performance_data: PerformanceData
    total_classes: TotalClasses
    date_range: Optional[DateRange] = None
    status: str
    message: Optional[str] = None