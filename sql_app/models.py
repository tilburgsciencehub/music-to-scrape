from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class UserInfo(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    age = Column(Integer)
    country = Column(String)
    description = Column(String)

    children = relationship('UserListening', back_populates='parent')

class UserListening(Base):
    __tablename__ = "listening"

    user = Column(String, ForeignKey('users.username'), index= True)
    date = Column(String)
    timestamp = Column(Integer)
    artist = Column(String)
    track = Column(String)
    id = Column(Integer, primary_key=True)

    parent = relationship('UserInfo', back_populates='children')
