from typing import Optional,List, Union
from pydantic import BaseModel
from datetime import date

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

class TrackDetails(BaseModel):
    artist: str
    track: str
    timestamp: float

class RecentTracks(BaseModel):
    username: str
    tracks: List[TrackDetails]

class TopArtistBase(BaseModel):
    name: str
    count: int

class TopArtistsUser(BaseModel):
    username: str
    top_artists: List[TopArtistBase]

class TopTrackBase(BaseModel):
    name: str
    count: int

class TopTracksUser(BaseModel):
    username: str
    top_tracks: List[TopTrackBase]

class WeeklyUserTrackChartBase(BaseModel):
    name: str
    artist: str
    play_count: int
    
class WeeklyTrackUserChart(BaseModel):
    username: str
    weekly_chart: List[WeeklyUserTrackChartBase]

class WeeklyUserArtistChartBase(BaseModel):
    artist: str
    play_count: int
    
class WeeklyArtistUserChart(BaseModel):
    username: str
    weekly_chart: List[WeeklyUserArtistChartBase]

# response classes Chart Top Tracks
class ChartTopTracksBase(BaseModel):
    name: str
    artist: str
    count: int

class ChartTopTracks(BaseModel):
    unix_start: int
    unix_end: int
    chart: List[ChartTopTracksBase]

# response classes Chart Top Artists
class ChartTopArtistsBase(BaseModel):
    name: str
    plays: int

class ChartTopArtists(BaseModel):
    unix_start: int
    unix_end: int
    chart: List[ChartTopArtistsBase]

#response class for Top tracks from Artist
class TopTracksArtist(BaseModel):
    artist: str
    top_tracks: List[TopTrackBase]

#response classes for Recent Users
class RecentUser(BaseModel):
    user: str
    date: date

class RecentActiveUsers(BaseModel):
    users: List[RecentUser]

class ArtistFeaturedArtist(BaseModel):
    artist: str
    featured: str

class ArtistFeaturedList(BaseModel):
    artists: List[ArtistFeaturedArtist]

class TopSongs(BaseModel):
    title: str
    plays: int

class ArtistInfo(BaseModel):
    artistid: str
    artistname: str
    artistlocation: str
    artistfeatured: str
    total_songs: int
    total_plays: int
    plays_last_week: int
    top_songs: List[TopSongs]