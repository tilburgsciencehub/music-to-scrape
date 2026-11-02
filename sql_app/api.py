# api.py
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_users, get_user_info_by_username, count_plays_by_username, get_recent_tracks_by_username, get_top_artists_for_user, get_top_tracks_for_user, get_weekly_track_chart_for_user, get_weekly_artist_chart_for_user, get_top_tracks_for_artist, get_chart_top_tracks, get_chart_top_artists, get_recent_active_users, get_featured_artists, get_artist_info
from database import get_db
from exceptions import CarInfoException
from schemas import User, CreateAndUpdateCar, PaginatedUserInfo, CountPlays, UserFindClass, RecentTracks, TopArtistsUser, TopTracksUser, WeeklyTrackUserChart, WeeklyArtistUserChart, TopTracksArtist, ChartTopTracks, ChartTopArtists, RecentActiveUsers, ArtistFeaturedList, ArtistInfo

router = APIRouter()
    
#user.getInfo
@router.get("/user/getinfo", response_model=UserFindClass, tags=["Users"], summary="Get information about a user", description="Returns demographic information, total plays, and the favourite artist for a user.")
def get_user_info(username: str = Query(..., description="Username to look up", examples=["user_123"]), session: Session = Depends(get_db)):

    try:
        user_info = get_user_info_by_username(session, username)
        return user_info
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#user.getTotalPlays
@router.get("/user/plays", response_model=CountPlays, tags=["Users"], summary="Count a user's plays", description="Returns the total number of recorded plays for a user.")
def get_total_plays_for_username(username: str = Query(..., description="Username whose plays should be counted", examples=["user_123"]), session: Session = Depends(get_db)):

    try:
        count_plays = count_plays_by_username(session, username)
        return count_plays
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#user.getRecentTracks    
@router.get("/user/recent-tracks", response_model= RecentTracks, tags=["Users"], summary="Get a user's recent tracks", description="Returns tracks recently played by a user. Use Unix timestamps for the optional start and end boundaries.")
def get_recent_tracks(username: str = Query(..., description="Username whose listening history should be returned", examples=["user_123"]), limit: int = Query(5, ge=1, le=100, description="Maximum number of tracks to return"), start: int = Query(0, description="Inclusive Unix timestamp lower bound"), end: int = Query(2000000000, description="Inclusive Unix timestamp upper bound"), session: Session = Depends(get_db)):

    try:
        tracks = get_recent_tracks_by_username(session, username, limit, start, end)
        return {"username": username, "tracks": tracks}

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#user.getTopArtists
@router.get("/user/top-artists", response_model= TopArtistsUser, tags=["Users"], summary="Get a user's top artists", description="Returns the artists with the most plays for a user. The period can be overall or a supported time period such as weekly.")
def get_user_top_artists(username: str = Query(..., description="Username whose top artists should be returned", examples=["user_123"]), limit: int = Query(5, ge=1, le=100, description="Maximum number of artists to return"), session: Session = Depends(get_db), period: str = Query("overall", description="Time period for the ranking")):

    try:
        top_artists = get_top_artists_for_user(session, username, limit, period)
        return {"username": username, "top_artists": top_artists}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#user.getTopTracks
@router.get("/user/top-tracks", response_model= TopTracksUser, tags=["Users"], summary="Get a user's top tracks", description="Returns the tracks with the most plays for a user. The period can be overall or a supported time period such as weekly.")
def get_user_top_tracks(username: str = Query(..., description="Username whose top tracks should be returned", examples=["user_123"]), limit: int = Query(5, ge=1, le=100, description="Maximum number of tracks to return"), session: Session = Depends(get_db), period: str = Query("overall", description="Time period for the ranking")):

    try:
        top_tracks = get_top_tracks_for_user(session, username, limit, period)
        return {"username": username, "top_tracks": top_tracks}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#user.getWeeklyTrackChart
@router.get("/user/weekly-track-chart", response_model = WeeklyTrackUserChart, tags=["Users"], summary="Get a user's weekly track chart", description="Returns the user's most-played tracks for the current weekly chart period.")
def get_weekly_track_chart_user(username: str = Query(..., description="Username whose weekly chart should be returned", examples=["user_123"]), session: Session = Depends(get_db)):

    try:
        weekly_chart = get_weekly_track_chart_for_user(session, username)
        return {"username": username, "weekly_chart": weekly_chart}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)


#user.getWeeklyArtistChart
@router.get("/user/weekly-artist-chart", response_model = WeeklyArtistUserChart, tags=["Users"], summary="Get a user's weekly artist chart", description="Returns the user's most-played artists for the current weekly chart period.")
def get_weekly_artist_chart_user(username: str = Query(..., description="Username whose weekly chart should be returned", examples=["user_123"]), session: Session = Depends(get_db), limit: int = Query(5, ge=1, le=100, description="Maximum number of artists to return")):

    try:
        weekly_chart = get_weekly_artist_chart_for_user(session, username, limit)
        return {"username": username, "weekly_chart": weekly_chart}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    

# API to get the list of user info
@router.get("/users", response_model=PaginatedUserInfo, tags=["Users"], summary="List users", description="Returns a paginated list of users. Use offset to skip records and limit to control the page size.")
def list_users(limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return"), offset: int = Query(0, ge=0, description="Number of users to skip"), session: Session = Depends(get_db)):

    cars_list = get_all_users(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": cars_list}

    return response

    
#user.getRecentlyActive    
@router.get("/users/recently-active", response_model = RecentActiveUsers, tags=["Users"], summary="List recently active users", description="Returns users with recent listening activity, ordered by activity date.")
def get_recently_active_users(limit: int = Query(5, ge=1, le=100, description="Maximum number of users to return"), session: Session = Depends(get_db)):

    try:
        users = get_recent_active_users(session, limit)
        return {"users": users}

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#artist.getTopTracks
@router.get("/artist/top-tracks", response_model= TopTracksArtist, tags=["Artists"], summary="Get an artist's top tracks", description="Returns the most-played tracks for an artist. Artist names may use underscores instead of spaces.")
def get_artist_top_tracks(artist: str = Query(..., description="Artist name; spaces may be represented by underscores", examples=["The_Beatles"]), limit: int = Query(5, ge=1, le=100, description="Maximum number of tracks to return"), session: Session = Depends(get_db)):

    try:
        top_tracks = get_top_tracks_for_artist(session, artist, limit)

        if "_" in artist:
            artist_name = artist.replace("_", " ")
    
        else:
            artist_name = artist
    
        return {"artist": artist_name, "top_tracks": top_tracks}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#artist.getInfo
@router.get("/artist/info", response_model = ArtistInfo, tags=["Artists"], summary="Get artist information", description="Returns metadata, listening totals, and top songs for an artist identified by artist ID.")
def artist_info(artistid: str = Query(..., description="Artist identifier", examples=["artist_123"]), session: Session = Depends(get_db)):
    try:
        artists = get_artist_info(session, artistid)
        return artists

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#artist.featured
@router.get("/artists/featured", response_model = ArtistFeaturedList, tags=["Artists"], summary="List featured artists", description="Returns a list of artists featured on the Music to Scrape website.")
def featured_artist(limit: int = Query(5, ge=1, le=100, description="Maximum number of featured artists to return"), session: Session = Depends(get_db)):

    try:
        artists = get_featured_artists(session, limit)
        return {"artists": artists}

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)


#chart.getTopTracks
@router.get("/charts/top-tracks", response_model= ChartTopTracks, tags=["Charts"], summary="Get the top tracks chart", description="Returns the most frequently played tracks during the one-week period beginning at unixtimestamp. If omitted, the current time is used.")
def chart_get_top_tracks(unixtimestamp: int = Query(None, description="Unix timestamp at the beginning of the one-week chart period", examples=[1693000000]), limit: int = Query(5, ge=1, le=100, description="Maximum number of tracks to return"), session: Session = Depends(get_db)):
    """
    Example: `/charts/top-tracks?unixtimestamp=1693000000&limit=10`.
    """

    try:
        top_tracks = get_chart_top_tracks(session, limit, unixtimestamp)
    
        return {"chart": top_tracks['tracks'],
                'unix_start': top_tracks['unix_start'],
                'unix_end': top_tracks['unix_end']}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#chart.getTopArtists
@router.get("/charts/top-artists", response_model= ChartTopArtists, tags=["Charts"], summary="Get the top artists chart", description="Returns the most frequently played artists during the one-week period beginning at unixtimestamp. If omitted, the current time is used.")
def chart_get_top_artists(unixtimestamp: int = Query(None, description="Unix timestamp at the beginning of the one-week chart period", examples=[1693000000]), limit: int = Query(5, ge=1, le=100, description="Maximum number of artists to return"), session: Session = Depends(get_db)):
    """
    Example: `/charts/top-artists?unixtimestamp=1693000000&limit=10`.
    """
    try:
        top_artists = get_chart_top_artists(session, limit, unixtimestamp)
        
        return {"chart": top_artists['artists'],
                'unix_start': top_artists['unix_start'],
                'unix_end': top_artists['unix_end']}
    
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
