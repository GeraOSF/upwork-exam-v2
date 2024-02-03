from pydantic import BaseModel

class ProfileCreate(BaseModel):
    name: str
    description: str

class Profile(ProfileCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True