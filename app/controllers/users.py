from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import UserModel, ProfileModel
from app.schemas import UserCreate


def get_users(skip: int, limit: int, db: Session):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user_by_id(user_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(user: UserCreate, db: Session):
    db_user = UserModel(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(user_id: int, user: UserCreate, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: int, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

def toggle_favorite_profile(user_id: int, profile_id: int, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if not user or not profile:
        raise HTTPException(status_code=404, detail="User or profile not found")
    if profile in user.favorite_profiles:
        user.favorite_profiles.remove(profile)
    else:
        user.favorite_profiles.append(profile)
    db.commit()
    return {"ok": True}
