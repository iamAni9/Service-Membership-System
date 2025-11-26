from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ============= MEMBER SCHEMAS =============

class MemberCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Member name is required")
    phone: str = Field(..., min_length=10, description="Phone number is required")
    status: Optional[str] = "active"


class MemberResponse(BaseModel):
    id: int
    name: str
    phone: str
    join_date: datetime
    status: str
    total_check_ins: int

    class Config:
        from_attributes = True


# ============= PLAN SCHEMAS =============

class PlanCreate(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    duration_days: int = Field(..., gt=0, description="Duration must be positive")


class PlanResponse(BaseModel):
    id: int
    name: str
    price: float
    duration_days: int

    class Config:
        from_attributes = True


# ============= SUBSCRIPTION SCHEMAS =============

class SubscriptionCreate(BaseModel):
    member_id: int
    plan_id: int
    start_date: datetime


class SubscriptionResponse(BaseModel):
    id: int
    member_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True


# ============= ATTENDANCE SCHEMAS =============

class AttendanceCheckIn(BaseModel):
    member_id: int


class AttendanceResponse(BaseModel):
    id: int
    member_id: int
    check_in_time: datetime

    class Config:
        from_attributes = True
