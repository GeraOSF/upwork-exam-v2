from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.db import get_db
from app.schemas import ProfileCreate


profiles_router = APIRouter()

@profiles_router.get("/", response_model=List[schemas.Profile])
async def get_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return controllers.get_profiles(skip, limit, db)

@profiles_router.get("/{profile_id}", response_model=schemas.Profile)
async def get_profile_by_id(profile_id: int, db: Session = Depends(get_db)):
    return controllers.get_profile_by_id(profile_id, db)

@profiles_router.post("/{user_id}", response_model=schemas.Profile)
async def create_profile(user_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    return controllers.create_profile(user_id, profile, db)

@profiles_router.put("/{profile_id}", response_model=schemas.Profile)
async def update_profile(profile_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    return controllers.update_profile(profile_id, profile, db)

@profiles_router.delete("/{profile_id}")
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    return controllers.delete_profile(profile_id, db)
