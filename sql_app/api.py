# api.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session
from crud import get_all_users, get_user_info_by_username, count_plays_by_username, get_recent_tracks_by_username, get_top_artists_for_user, get_top_tracks_for_user, get_weekly_track_chart_for_user, get_weekly_artist_chart_for_user, get_top_tracks_for_artist, get_chart_top_tracks, get_chart_top_artists, get_recent_active_users, get_featured_artists, get_artist_info
from database import get_db
from exceptions import CarInfoException
from schemas import User, CreateAndUpdateCar, PaginatedUserInfo, CountPlays, UserFindClass, RecentTracks, TopArtistsUser, TopTracksUser, WeeklyTrackUserChart, WeeklyArtistUserChart, TopTracksArtist, ChartTopTracks, ChartTopArtists, RecentActiveUsers, ArtistFeaturedList, ArtistInfo

router = APIRouter()
    
# API to get the list of user info
@router.get("/users", response_model=PaginatedUserInfo)
def list_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_db)):

    cars_list = get_all_users(session, limit, offset)
    response = {"limit": limit, "offset": offset, "data": cars_list}

    return response

#user.getInfo
@router.get("/user/getinfo", response_model=UserFindClass)
def get_user_info(username: str, session: Session = Depends(get_db)):

    try:
        user_info = get_user_info_by_username(session, username)
        return user_info
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#user.getTotalPlays
@router.get("/totalplays", response_model=CountPlays)
def get_total_plays_for_username(username: str, session: Session = Depends(get_db)):

    try:
        count_plays = count_plays_by_username(session, username)
        return count_plays
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#user.getRecentTracks    
@router.get("/user-recent-tracks", response_model= RecentTracks)
def get_recent_tracks(username: str, limit: int = 5, start: int = 0 , end: int = 2000000000, session: Session = Depends(get_db)):

    try:
        tracks = get_recent_tracks_by_username(session, username, limit, start, end)
        return {"username": username, "tracks": tracks}

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#user.getTopArtists
@router.get("/user-top-artists", response_model= TopArtistsUser)
def get_user_top_artists(username: str, limit: int = 5, session: Session = Depends(get_db), period: str = "overall"):

    try:
        top_artists = get_top_artists_for_user(session, username, limit, period)
        return {"username": username, "top_artists": top_artists}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#user.getTopTracks
@router.get("/user-top-tracks", response_model= TopTracksUser)
def get_user_top_tracks(username: str, limit: int = 5, session: Session = Depends(get_db), period: str = "overall"):

    try:
        top_tracks = get_top_tracks_for_user(session, username, limit, period)
        return {"username": username, "top_tracks": top_tracks}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#user.getWeeklyTrackChart
@router.get("/weekly-track-chart-user", response_model = WeeklyTrackUserChart)
def get_weekly_track_chart_user(username: str, session: Session = Depends(get_db)):

    try:
        weekly_chart = get_weekly_track_chart_for_user(session, username)
        return {"username": username, "weekly_chart": weekly_chart}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#user.getWeeklyArtistChart
@router.get("/weekly-artist-chart-user", response_model = WeeklyArtistUserChart)
def get_weekly_artist_chart_user(username: str, session: Session = Depends(get_db), limit: int = 5):

    try:
        weekly_chart = get_weekly_artist_chart_for_user(session, username, limit)
        return {"username": username, "weekly_chart": weekly_chart}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#artist.getTopTracks
@router.get("/artist-top-tracks", response_model= TopTracksArtist)
def get_artist_top_tracks(artist: str, limit: int = 5, session: Session = Depends(get_db)):

    try:
        top_tracks = get_top_tracks_for_artist(session, artist, limit)

        if "_" in artist:
            artist_name = artist.replace("_", " ")
    
        else:
            artist_name = artist
    
        return {"artist": artist_name, "top_tracks": top_tracks}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#chart.getTopTracks
@router.get("/chart-top-tracks", response_model= ChartTopTracks)
def chart_get_top_tracks(week: int, limit: int = 5, session: Session = Depends(get_db), year: int = 2023):

    try:
        top_tracks = get_chart_top_tracks(session, limit, year, week)
    
        return {"week": week, "chart": top_tracks}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#chart.getTopArtists
@router.get("/chart-top-artists", response_model= ChartTopArtists)
def chart_get_top_artists(week: int, limit: int = 5, session: Session = Depends(get_db), year: int = 2023):

    try:
        top_artists = get_chart_top_artists(session, limit, year, week)
    
        return {"week": week, "chart": top_artists}
    
    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)
    
#user.getRecentlyActive    
@router.get("/recently-active-users", response_model = RecentActiveUsers)
def get_recently_active_users(limit: int = 5, session: Session = Depends(get_db)):

    """
    Get recently active user

    ## Request example

    ```python
    import requests

    url = "http://localhost:8000/recently-active-users/"

    payload = {
        "limit": 5
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(Succes, response.json())
    else:
        print("Error", response.text)
    ```
    """

    try:
        users = get_recent_active_users(session, limit)
        return {"users": users}

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#artist.featured
@router.get("/featured-artists", response_model = ArtistFeaturedList)
def featured_artist(limit: int = 5, session: Session = Depends(get_db)):

    try:
        artists = get_featured_artists(session, limit)
        return {"artists": artists}

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)

#artist.getInfo
@router.get("/artist-info", response_model = ArtistInfo)
def artist_info(artist: str, session: Session = Depends(get_db)):

    try:
        artists = get_artist_info(session, artist)
        return artists

    except CarInfoException as cie:
        raise HTTPException(**cie.__dict__)