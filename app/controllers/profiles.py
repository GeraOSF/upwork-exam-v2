from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import ProfileModel, UserModel
from app.schemas import ProfileCreate


def get_profiles(skip: int, limit: int, db: Session):
    profiles = db.query(ProfileModel).offset(skip).limit(limit).all()
    return profiles

def get_profile_by_id(profile_id: int, db: Session):
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

def create_profile(user_id: int, profile: ProfileCreate, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_profile = ProfileModel(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(profile_id: int, profile: ProfileCreate, db: Session):
    db_profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(profile_id: int, db: Session):
    db_profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
    return {"ok": True}
