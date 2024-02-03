from pydantic import BaseModel, ConfigDict

class ProfileCreate(BaseModel):
    name: str
    description: str

class Profile(ProfileCreate):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)