from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List
from app.schemas.profiles import Profile


class UserCreate(BaseModel):
    email: EmailStr

class User(UserCreate):
    id: int
    profiles: List[Profile] = []
    favorite_profiles: List[Profile] = []
    
    model_config = ConfigDict(from_attributes=True)