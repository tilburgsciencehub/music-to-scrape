from typing import Optional,List, Union
from pydantic import BaseModel, Field
from datetime import date as Date

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
    username: str = Field(description="The user's username", examples=["user_123"])
    age: int = Field(description="The user's age in years", examples=[24])
    country: str = Field(description="The user's country", examples=["The Netherlands"])
    description: str = Field(description="A short user description", examples=["Music enthusiast"])

# TO support list and get APIs
class UserFindClass(BaseModel):
    user_info: SecondResponse = Field(description="Demographic information about the user")
    total_plays: int = Field(description="Total number of recorded plays", examples=[1250])
    favourite_artist: str = Field(description="The user's most-played artist", examples=["The Beatles"])

    class Config:
        orm_mode = True

# TO support list and get APIs
class User(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    age: int = Field(description="The user's age in years", examples=[24])
    country: str = Field(description="The user's country", examples=["The Netherlands"])
    description: str = Field(description="A short user description", examples=["Music enthusiast"])

    class Config:
        orm_mode = True


# To support list cars API
class PaginatedUserInfo(BaseModel):
    limit: int = Field(description="Maximum number of users requested", examples=[10])
    offset: int = Field(description="Number of users skipped", examples=[0])
    data: List[User] = Field(description="Users in this page")

# TO support creation and update APIs
class CountPlays(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    plays: int = Field(description="Total number of recorded plays", examples=[1250])

class TrackDetails(BaseModel):
    artist: str = Field(description="Artist name", examples=["The Beatles"])
    track: str = Field(description="Track name", examples=["Yesterday"])
    timestamp: float = Field(description="Unix timestamp of the play", examples=[1693000000])

class RecentTracks(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    tracks: List[TrackDetails] = Field(description="Recently played tracks")

class TopArtistBase(BaseModel):
    name: str = Field(description="Artist name", examples=["The Beatles"])
    plays: int = Field(description="Number of plays", examples=[1250])

class TopArtistsUser(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    top_artists: List[TopArtistBase] = Field(description="Artists ranked by number of plays")

class TopTrackBase(BaseModel):
    name: str = Field(description="Track name", examples=["Yesterday"])
    plays: int = Field(description="Number of plays", examples=[1250])

class TopTracksUser(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    top_tracks: List[TopTrackBase] = Field(description="Tracks ranked by number of plays")

class WeeklyUserTrackChartBase(BaseModel):
    name: str = Field(description="Track name", examples=["Yesterday"])
    artist: str = Field(description="Artist name", examples=["The Beatles"])
    play_count: int = Field(description="Number of plays during the chart period", examples=[1250])
    
class WeeklyTrackUserChart(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    weekly_chart: List[WeeklyUserTrackChartBase] = Field(description="The user's weekly track ranking")

class WeeklyUserArtistChartBase(BaseModel):
    artist: str = Field(description="Artist name", examples=["The Beatles"])
    play_count: int = Field(description="Number of plays during the chart period", examples=[1250])
    
class WeeklyArtistUserChart(BaseModel):
    username: str = Field(description="The user's username", examples=["user_123"])
    weekly_chart: List[WeeklyUserArtistChartBase] = Field(description="The user's weekly artist ranking")

# response classes Chart Top Tracks
class ChartTopTracksBase(BaseModel):
    name: str = Field(description="Track name", examples=["Yesterday"])
    artist: str = Field(description="Artist name", examples=["The Beatles"])
    plays: int = Field(description="Number of plays during the chart period", examples=[1250])

class ChartTopTracks(BaseModel):
    unix_start: int = Field(description="Unix timestamp at the start of the chart period", examples=[1693000000])
    unix_end: int = Field(description="Unix timestamp at the end of the chart period", examples=[1693604800])
    chart: List[ChartTopTracksBase] = Field(description="Tracks ranked by number of plays")

# response classes Chart Top Artists
class ChartTopArtistsBase(BaseModel):
    name: str = Field(description="Artist name", examples=["The Beatles"])
    plays: int = Field(description="Number of plays during the chart period", examples=[1250])

class ChartTopArtists(BaseModel):
    unix_start: int = Field(description="Unix timestamp at the start of the chart period", examples=[1693000000])
    unix_end: int = Field(description="Unix timestamp at the end of the chart period", examples=[1693604800])
    chart: List[ChartTopArtistsBase] = Field(description="Artists ranked by number of plays")

#response class for Top tracks from Artist
class TopTracksArtist(BaseModel):
    artist: str = Field(description="Artist name", examples=["The Beatles"])
    top_tracks: List[TopTrackBase] = Field(description="Tracks ranked by number of plays")

#response classes for Recent Users
class RecentUser(BaseModel):
    user: str = Field(description="The user's username", examples=["user_123"])
    date: Date = Field(description="Date of recent activity", examples=["2023-08-25"])

class RecentActiveUsers(BaseModel):
    users: List[RecentUser] = Field(description="Users ranked by recent activity")

class ArtistFeaturedArtist(BaseModel):
    artist: str = Field(description="Artist name", examples=["The Beatles"])
    artist_id: str = Field(description="Artist identifier used by the API", examples=["artist_123"])

class ArtistFeaturedList(BaseModel):
    artists: List[ArtistFeaturedArtist] = Field(description="Featured artists")

class TopSongs(BaseModel):
    title: str = Field(description="Song title", examples=["Yesterday"])
    plays: int = Field(description="Number of plays", examples=[1250])

class ArtistInfo(BaseModel):
    artistid: str = Field(description="Artist identifier", examples=["artist_123"])
    artistname: str = Field(description="Artist name", examples=["The Beatles"])
    artistlocation: str = Field(description="Artist location", examples=["Liverpool"])
    artistfeatured: str = Field(description="Whether the artist is featured", examples=["true"])
    total_songs: int = Field(description="Total number of songs by the artist", examples=[250])
    total_plays: int = Field(description="Total plays for the artist", examples=[12500])
    plays_last_week: int = Field(description="Artist plays during the previous week", examples=[1250])
    top_songs: List[TopSongs] = Field(description="The artist's most-played songs")
