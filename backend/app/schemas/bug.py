"""
Pydantic schemas for bugs
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import BugSeverity, BugStatus


class BugBase(BaseModel):
    """Base bug schema"""
    title: str
    description: str
    severity: BugSeverity = BugSeverity.MEDIUM


class BugCreate(BugBase):
    """Bug creation schema"""
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    reproduction_steps: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None


class BugUpdate(BaseModel):
    """Bug update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[BugSeverity] = None
    status: Optional[BugStatus] = None
    assigned_to: Optional[int] = None
    reproduction_steps: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None


class BugResponse(BugBase):
    """Bug response schema"""
    id: int

    status: BugStatus

    project_id: Optional[int]
    assigned_to: Optional[int]
    reported_by: int

    reproduction_steps: Optional[str]
    expected_result: Optional[str]
    actual_result: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True