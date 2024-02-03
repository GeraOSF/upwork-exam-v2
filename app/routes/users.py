from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import controllers, schemas
from app.models import UserModel, ProfileModel
from app.schemas import UserCreate
from app.db import get_db


users_router = APIRouter()

@users_router.get("/", response_model=List[schemas.User])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return controllers.get_users(skip, limit, db)

@users_router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    return controllers.get_user_by_id(user_id, db)

@users_router.post("/", response_model=schemas.User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return controllers.create_user(user, db)

@users_router.put("/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return controllers.update_user(user_id, user, db)

@users_router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return controllers.delete_user(user_id, db)

@users_router.put("/{user_id}/favorites/{profile_id}")
async def toggle_favorite_profile(user_id: int, profile_id: int, db: Session = Depends(get_db)):
    return controllers.toggle_favorite_profile(user_id, profile_id, db)