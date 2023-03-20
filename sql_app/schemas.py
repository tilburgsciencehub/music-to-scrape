from typing import Optional,List, Union
from pydantic import BaseModel

# TO support creation and update APIs
class CreateAndUpdateCar(BaseModel):
    id: int
    user: str
    date: str
    timestamp: int
    artist: str
    track: str

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
    favourite_artist: str

    class Config:
        orm_mode = True

# TO support list and get APIs
class User(BaseModel):
    username: str
    age: int
    country: str
    description: str

    class Config:
        orm_mode = True


# To support list cars API
class PaginatedUserInfo(BaseModel):
    limit: int
    offset: int
    data: List[User]

# TO support creation and update APIs
class CountPlays(BaseModel):
    username: str
    plays: int
