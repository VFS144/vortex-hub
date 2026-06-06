"""
Project related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ProjectStage(str, enum.Enum):
    """Project development stage"""
    CONCEPT = "concept"
    PROTOTYPE = "prototype"
    VERTICAL_SLICE = "vertical_slice"
    ALPHA = "alpha"
    BETA = "beta"
    RELEASE = "release"
    POST_LAUNCH = "post_launch"


class Project(Base):
    """Project model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    stage = Column(Enum(ProjectStage), default=ProjectStage.CONCEPT, nullable=False)
    budget = Column(String(255), nullable=True)
    progress = Column(Integer, default=0, nullable=False)  # 0-100%
    lead_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True
