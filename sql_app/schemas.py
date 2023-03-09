from typing import Optional,List, Union
from pydantic import BaseModel

# TO support creation and update APIs
class CreateAndUpdateCar(BaseModel):
    user: str
    date: str
    timestamp: int
    artist: str
    track: str
    id: str

# TO support creation and update APIs
class SecondResponse(BaseModel):
    username: str
    age: int
    country: str
    description: str

# TO support list and get APIs
class UserFindClass(BaseModel):
    user_info: SecondResponse
    total_plays: int
    favorite_artist: str
    favorite_track: str

    class Config:
        orm_mode = True

# TO support list and get APIs
class User(UserFindClass):
    username: str

    class Config:
        orm_mode = True


# To support list cars API
class PaginatedUserInfo(BaseModel):
    limit: int
    offset: int
    data: List[User]

# Count Plays Response Model
class CountPlays(BaseModel):
    username: str
    plays: int

# Recent Users Response Model in List
class RecentResponseModel(BaseModel):
    user: str
    timestamp: int

# Recent User Info
class RecentlyActive(RecentResponseModel):
    user: str
    
    class Config:
        orm_mode = True

# Recent User Info (Main Response Model)
class PaginatedRecentUserInfo(BaseModel):
    limit: int
    offset: int
    data: List[RecentlyActive]



