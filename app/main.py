from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional


DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(docs_url="/")

class ProfileCreate(BaseModel):
    name: str
    description: str

class Profile(ProfileCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr

class User(UserCreate):
    id: int
    profiles: List[Profile] = []
    favorite_profiles: List[Profile] = []
    class Config:
        from_attributes = True

favorites_association = Table('favorites', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('profile_id', ForeignKey('profiles.id'), primary_key=True)
)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    profiles = relationship("ProfileModel", back_populates="owner")
    favorite_profiles = relationship(
        'ProfileModel',
        secondary=favorites_association,
        back_populates='favorited_by'
    )

class ProfileModel(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel", back_populates="profiles")
    favorited_by = relationship(
        'UserModel',
        secondary=favorites_association,
        back_populates='favorite_profiles'
    )

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

@app.put("/users/{user_id}/favorites/{profile_id}")
async def toggle_favorite_profile(user_id: int, profile_id: int, db: Session = Depends(get_db)):
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

@app.get("/profiles/", response_model=List[Profile])
async def get_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    profiles = db.query(ProfileModel).offset(skip).limit(limit).all()
    return profiles

@app.get("/profiles/{profile_id}", response_model=Profile)
async def get_profile_by_id(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/profiles/{user_id}", response_model=Profile)
async def create_profile(user_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_profile = ProfileModel(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.put("/profiles/{profile_id}", response_model=Profile)
async def update_profile(profile_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    db_profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.delete("/profiles/{profile_id}")
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(db_profile)
    db.commit()
    return {"ok": True}
