from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

# Enums
class RequestTypeEnum(str, Enum):
    NEW_REQUEST = "NEW_REQUEST"
    CHANGE_REQUEST = "CHANGE_REQUEST"
    BUG_FIX = "BUG_FIX"

class StatusEnum(str, Enum):
    SUBMITTED = "SUBMITTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_REVIEW = "IN_REVIEW"
    SENT_FOR_APPROVAL = "SENT_FOR_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

# Request Schemas
class RequestCreateSchema(BaseModel):
    """Schema for creating a new request"""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    request_type: RequestTypeEnum
    business_unit: Optional[str] = None
    priority: Optional[str] = None  # HIGH, MEDIUM, LOW
    submitted_by: int  # User ID

    class Config:
        from_attributes = True

class RequestUpdateSchema(BaseModel):
    """Schema for updating a request"""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[StatusEnum] = None

    class Config:
        from_attributes = True

class RequestDetailSchema(BaseModel):
    """Schema for request response with all details"""
    id: int
    title: str
    description: str
    request_type: RequestTypeEnum
    business_unit: Optional[str]
    priority: Optional[str]
    status: StatusEnum
    submitted_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RequestListSchema(BaseModel):
    """Schema for request list response"""
    id: int
    title: str
    description: str
    request_type: RequestTypeEnum
    status: StatusEnum
    priority: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# WSJF Schemas
class WSJFCreateSchema(BaseModel):
    """Schema for WSJF scoring"""
    user_business_value: int = Field(..., ge=1, le=9)
    time_criticality: int = Field(..., ge=1, le=9)
    risk_reduction: int = Field(..., ge=1, le=9)
    job_size: int = Field(..., ge=1, le=9)

    class Config:
        from_attributes = True

class WSJFSchema(BaseModel):
    """WSJF response schema"""
    id: int
    request_id: int
    user_business_value: int
    time_criticality: int
    risk_reduction: int
    job_size: int
    wsjf_score: Optional[float]

    class Config:
        from_attributes = True
