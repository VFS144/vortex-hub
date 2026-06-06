"""
Additional lore and documentation models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Quest(Base):
    """Quest model"""
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    objectives = Column(Text, nullable=True)
    rewards = Column(Text, nullable=True)
    giver_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True


class Asset(Base):
    """Asset management"""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    asset_type = Column(String(100), nullable=False)  # sprite, animation, music, etc.
    file_path = Column(String(500), nullable=True)
    version = Column(Integer, default=1, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True


class MeetingNotes(Base):
    """Meeting notes storage"""
    __tablename__ = "meeting_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    decisions = Column(Text, nullable=True)
    action_items = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    meeting_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    class Config:
        from_attributes = True


class Milestone(Base):
    """Project milestones"""
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    target_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="pending", nullable=False)  # pending, in_progress, completed
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True


class ContentSchedule(Base):
    """Content creation calendar"""
    __tablename__ = "content_schedule"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    platform = Column(String(100), nullable=False)  # youtube, tiktok, instagram, x
    content_type = Column(String(100), nullable=False)  # video, post, idea, draft
    scheduled_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    description = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True
