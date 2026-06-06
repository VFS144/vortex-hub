"""
Pydantic schemas for lore database
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CharacterBase(BaseModel):
    """Base character schema"""
    name: str
    age: Optional[str] = None
    race: Optional[str] = None
    role: Optional[str] = None
    personality: Optional[str] = None
    abilities: Optional[str] = None
    backstory: Optional[str] = None
    relationships: Optional[str] = None


class CharacterCreate(CharacterBase):
    """Character creation schema"""
    project_id: Optional[int] = None


class CharacterResponse(CharacterBase):
    """Character response schema"""
    id: int
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationBase(BaseModel):
    """Base location schema"""
    name: str
    description: Optional[str] = None
    region: Optional[str] = None
    significance: Optional[str] = None


class LocationCreate(LocationBase):
    """Location creation schema"""
    project_id: Optional[int] = None


class LocationResponse(LocationBase):
    """Location response schema"""
    id: int
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FactionBase(BaseModel):
    """Base faction schema"""
    name: str
    description: Optional[str] = None
    goals: Optional[str] = None
    members: Optional[str] = None


class FactionCreate(FactionBase):
    """Faction creation schema"""
    project_id: Optional[int] = None


class FactionResponse(FactionBase):
    """Faction response schema"""
    id: int
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
