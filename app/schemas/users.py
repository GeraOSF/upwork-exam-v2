from pydantic import BaseModel, EmailStr
from typing import List
from app.schemas.profiles import Profile


class UserCreate(BaseModel):
    email: EmailStr

class User(UserCreate):
    id: int
    profiles: List[Profile] = []
    favorite_profiles: List[Profile] = []
    class Config:
        from_attributes = True