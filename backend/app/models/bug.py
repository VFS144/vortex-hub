"""
Bug tracker related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class BugSeverity(str, enum.Enum):
    """Bug severity level"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BugStatus(str, enum.Enum):
    """Bug status workflow"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"


class Bug(Base):
    """Bug model"""
    __tablename__ = "bugs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    severity = Column(Enum(BugSeverity), default=BugSeverity.MEDIUM, nullable=False)
    status = Column(Enum(BugStatus), default=BugStatus.OPEN, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    reproduction_steps = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True)
    actual_result = Column(Text, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True
