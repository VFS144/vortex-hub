"""
Lore management routes with role-based access control
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import User, Character, Location, Faction, UserRole
from app.schemas.lore import (
    CharacterCreate, CharacterResponse,
    LocationCreate, LocationResponse,
    FactionCreate, FactionResponse,
)
from app.utils.dependencies import get_current_approved_user, require_role

router = APIRouter(prefix="/api/lore", tags=["lore"])

# Role-based access control for lore
LORE_WRITERS = {UserRole.LORE_WRITER, UserRole.ADMINISTRATOR}


# Characters endpoints
@router.get("/characters", response_model=List[CharacterResponse])
async def get_characters(
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
    project_id: int = None,
):
    """Get all characters - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access lore",
        )
    
    query = db.query(Character)
    if project_id:
        query = query.filter(Character.project_id == project_id)
    return query.all()


@router.post("/characters", response_model=CharacterResponse)
async def create_character(
    character_data: CharacterCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Create a new character - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot create lore",
        )
    
    character = Character(**character_data.dict(exclude_unset=True))
    db.add(character)
    db.commit()
    db.refresh(character)
    return character


@router.get("/characters/{character_id}", response_model=CharacterResponse)
async def get_character(
    character_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get character by ID - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access lore",
        )
    
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    return character


@router.patch("/characters/{character_id}", response_model=CharacterResponse)
async def update_character(
    character_id: int,
    character_data: CharacterCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Update character - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot edit lore",
        )
    
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    
    update_data = character_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(character, field, value)
    
    db.commit()
    db.refresh(character)
    return character


@router.delete("/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_character(
    character_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Delete character - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot delete lore",
        )
    
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found",
        )
    db.delete(character)
    db.commit()


# Locations endpoints
@router.get("/locations", response_model=List[LocationResponse])
async def get_locations(
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
    project_id: int = None,
):
    """Get all locations - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access lore",
        )
    
    query = db.query(Location)
    if project_id:
        query = query.filter(Location.project_id == project_id)
    return query.all()


@router.post("/locations", response_model=LocationResponse)
async def create_location(
    location_data: LocationCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Create a new location - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot create lore",
        )
    
    location = Location(**location_data.dict(exclude_unset=True))
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.get("/locations/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get location by ID - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access lore",
        )
    
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    return location


@router.patch("/locations/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location_data: LocationCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Update location - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot edit lore",
        )
    
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    
    update_data = location_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    db.commit()
    db.refresh(location)
    return location


@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Delete location - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot delete lore",
        )
    
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found",
        )
    db.delete(location)
    db.commit()


# Factions endpoints
@router.get("/factions", response_model=List[FactionResponse])
async def get_factions(
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
    project_id: int = None,
):
    """Get all factions - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access lore",
        )
    
    query = db.query(Faction)
    if project_id:
        query = query.filter(Faction.project_id == project_id)
    return query.all()


@router.post("/factions", response_model=FactionResponse)
async def create_faction(
    faction_data: FactionCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Create a new faction - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot create lore",
        )
    
    faction = Faction(**faction_data.dict(exclude_unset=True))
    db.add(faction)
    db.commit()
    db.refresh(faction)
    return faction


@router.get("/factions/{faction_id}", response_model=FactionResponse)
async def get_faction(
    faction_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Get faction by ID - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot access lore",
        )
    
    faction = db.query(Faction).filter(Faction.id == faction_id).first()
    if not faction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faction not found",
        )
    return faction


@router.patch("/factions/{faction_id}", response_model=FactionResponse)
async def update_faction(
    faction_id: int,
    faction_data: FactionCreate,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Update faction - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot edit lore",
        )
    
    faction = db.query(Faction).filter(Faction.id == faction_id).first()
    if not faction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faction not found",
        )
    
    update_data = faction_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(faction, field, value)
    
    db.commit()
    db.refresh(faction)
    return faction


@router.delete("/factions/{faction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faction(
    faction_id: int,
    current_user: User = Depends(get_current_approved_user),
    db: Session = Depends(get_db),
):
    """Delete faction - Lore Writers and Admins only"""
    if current_user.role not in LORE_WRITERS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Role {current_user.role} cannot delete lore",
        )
    
    faction = db.query(Faction).filter(Faction.id == faction_id).first()
    if not faction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faction not found",
        )
    db.delete(faction)
    db.commit()
