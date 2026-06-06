"""
Lore database related models
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Character(Base):
    """Character model for lore database"""
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    age = Column(String(50), nullable=True)
    race = Column(String(100), nullable=True)
    role = Column(String(255), nullable=True)
    personality = Column(Text, nullable=True)
    abilities = Column(Text, nullable=True)
    backstory = Column(Text, nullable=True)
    relationships = Column(Text, nullable=True)  # JSON field in practice
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True


class Location(Base):
    """Location model for lore database"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    region = Column(String(255), nullable=True)
    significance = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True


class Faction(Base):
    """Faction model for lore database"""
    __tablename__ = "factions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    goals = Column(Text, nullable=True)
    members = Column(Text, nullable=True)  # JSON field in practice
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    class Config:
        from_attributes = True
