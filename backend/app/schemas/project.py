"""
Pydantic schemas for projects
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import ProjectStage


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str
    description: Optional[str] = None
    stage: ProjectStage = ProjectStage.CONCEPT
    budget: Optional[str] = None
    progress: int = 0


class ProjectCreate(ProjectBase):
    """Project creation schema"""
    lead_id: Optional[int] = None


class ProjectUpdate(BaseModel):
    """Project update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[ProjectStage] = None
    budget: Optional[str] = None
    progress: Optional[int] = None
    lead_id: Optional[int] = None


class ProjectResponse(ProjectBase):
    """Project response schema"""
    id: int
    lead_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
