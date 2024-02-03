from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db import Base, engine


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