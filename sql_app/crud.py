# crud.py
from typing import List
from sqlalchemy.orm import Session
from exceptions import CarInfoNotFoundError
from models import UserInfo, UserListening
from sqlalchemy import func
import time
import datetime


# Function to get list of car info
def get_all_users(session: Session, limit: int, offset: int) -> List[UserInfo]:
    return session.query(UserInfo).offset(offset).limit(limit).all()

# Function to  get info of particular user
def get_user_info_by_username(session: Session, _username: str) -> UserInfo:
    user_info = session.query(UserInfo).get(_username)
    count_plays = session.query(UserListening).filter_by(user=_username).count()
    favorite_artist = session.query(UserListening.artist, func.count(UserListening.artist)).filter_by(user=_username).group_by(UserListening.artist).order_by(func.count(UserListening.artist).desc()).first()
    user_info2 = user_info.__dict__

    user_dict = {'user_info': user_info2, 'total_plays' : count_plays, 'favourite_artist' : favorite_artist[0]}

    if user_dict is None:
        raise CarInfoNotFoundError

    return user_dict

# Function to get total user plays
def count_plays_by_username(session: Session, _username: str) -> UserListening:
    count_plays = session.query(UserListening).filter_by(user=_username).count()

    if count_plays is None:
        raise CarInfoNotFoundError

    else: 
        count_dict = {'username': _username, 'plays': count_plays}
        return count_dict

# Function for user.getRecentTracks
def get_recent_tracks_by_username(session: Session, _username: str, _limit: int, start: int, end):

    recent_tracks = session.query(UserListening).filter(
        UserListening.user == _username,
        UserListening.timestamp >= start,
        UserListening.timestamp <= end,
        ).order_by(UserListening.timestamp.desc()).limit(_limit).all()
    
    tracks = []

    for track in recent_tracks:
        tracks.append({
            "artist": track.artist,
            "track": track.track,
            "timestamp": track.timestamp
        })

    
    if recent_tracks is None:
        raise CarInfoNotFoundError
    
    else:
        return tracks

# Function for user.GetTopArtists    
def get_top_artists_for_user(session: Session, username: str, limit: int = 5, period: str = "overall"):

    #get period
    if (period == "overall"):
        end = 2000000000
        start = 0

    elif (period =="7day"):
        end = int(time.time())
        start = end - (7 * 24 * 60 * 60)
    
    elif (period =="1month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=30)).timestamp())

    elif (period =="3month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=90)).timestamp())

    elif (period =="6month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=180)).timestamp())

    elif (period =="12month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=365)).timestamp())

    #query
    top_artists = session.query(UserListening.artist, func.count(UserListening.artist)).filter(
        UserListening.user == username,
        UserListening.timestamp >= start,
        UserListening.timestamp <= end).group_by(UserListening.artist).order_by(func.count(UserListening.artist).desc()).limit(limit).all()
    
    #insert data in list
    artists = []

    for artist, count in top_artists:
        artists.append({
            "name": artist,
            "count": count
        })

    if top_artists is None:
        raise CarInfoNotFoundError
    
    else:
        return artists
    
# Function for user.GetTopTracks  7day | 1month | 3month | 6month | 12month
def get_top_tracks_for_user(session: Session, username: str, limit: int = 5, period: str = "overall"):

    #get period
    if (period == "overall"):
        end = 2000000000
        start = 0

    elif (period =="7day"):
        end = int(time.time())
        start = end - (7 * 24 * 60 * 60)
    
    elif (period =="1month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=30)).timestamp())

    elif (period =="3month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=90)).timestamp())

    elif (period =="6month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=180)).timestamp())

    elif (period =="12month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=365)).timestamp())
    
    #query
    top_tracks = session.query(UserListening.track, func.count(UserListening.track)).filter(
        UserListening.user == username,
        UserListening.timestamp >= start,
        UserListening.timestamp <= end).group_by(UserListening.track).order_by(func.count(UserListening.track).desc()).limit(limit).all()
    
    #insert data in list
    tracks = []
    
    for track, count in top_tracks:
        tracks.append({
            "name": track,
            "count": count
        })

    if top_tracks is None:
        raise CarInfoNotFoundError
    
    else:
        return tracks
       
#Function fur user.GetWeeklyTrackChart
def get_weekly_track_chart_for_user(session: Session, username: str):
    # get the last week's date range
    last_week_start = datetime.now() - timedelta(days=7)
    last_week_end = datetime.now()

    # get the user's plays from the last week
    plays = session.query(UserListening).filter(
        UserListening.user == username,
        UserListening.timestamp >= last_week_start,
        UserListening.timestamp <= last_week_end,
    ).all()

    # group plays by track
    track_plays = {}
    for play in plays:
        track = play.track
        if track in track_plays:
            track_plays[track] += 1
        else:
            track_plays[track] = 1

    # sort tracks by play count and get the top 10
    top_tracks = sorted(track_plays.items(), key=lambda x: x[1], reverse=True)[:10]

    # get the track details for the top tracks
    track_details = []
    for track_name, play_count in top_tracks:
        track = session.query(UserListening).filter(UserListening.track == track_name).first()
        track_details.append({
            "name": track.track,
            "artist": track.artist,
            "play_count": play_count
        })

    return track_details

#Function fur user.GetWeeklyTrackChart
def get_weekly_artist_chart_for_user(session: Session, username: str, limit: int):
    # get the last week's date range
    last_week_start = datetime.now() - timedelta(days=7)
    last_week_end = datetime.now()

    # get the user's plays from the last week
    plays = session.query(UserListening).filter(
        UserListening.user == username
    ).all()

    # group plays by track
    artist_plays = {}
    for play in plays:
        artist = play.artist
        if artist in artist_plays:
            artist_plays[artist] += 1
        else:
            artist_plays[artist] = 1

    # sort artists by play count and get the top 10
    top_artists = sorted(artist_plays.items(), key=lambda x: x[1], reverse=True)[:limit]

    # get the track details for the top tracks
    artist_details = []
    for artist, play_count in top_artists:
        artist_details.append({
            "artist": artist,
            "play_count": play_count
        })

    return artist_details

# Function for artist.GetTopTracks
def get_top_tracks_for_artist(session: Session, artist: str, limit: int = 5):
    
    #replace _ with space
    if "_" in artist:
        artist_name = artist.replace("_", " ")
    
    else:
        artist_name = artist
    #query
    top_tracks = session.query(UserListening.track, func.count(UserListening.track)).filter(
        UserListening.artist == artist_name).group_by(UserListening.track).order_by(func.count(UserListening.track).desc()).limit(limit).all()
    
    #insert data in list
    tracks = []
    
    for track, count in top_tracks:
        tracks.append({
            "name": track,
            "count": count
        })

    if top_tracks is None:
        raise CarInfoNotFoundError
    
    else:
        return tracks

#function for chart.getTopTracks (for a given week, the charts)    
def get_chart_top_tracks(session: Session, limit: int, year: int, week: int):
    
    # Get the date of the first day of the given year
    first_day = datetime.datetime(year, 1, 1).date()

    # Get the date of the first Monday of the year (week 1)
    first_monday = first_day + datetime.timedelta(days=(7 - first_day.weekday()))

    # Get the start date of the requested week
    start_date = first_monday + datetime.timedelta(weeks=(week - 1))
    start_datetime = datetime.datetime.combine(start_date, datetime.time())

    # Get the end date of the requested week
    end_date = start_date + datetime.timedelta(days=6)
    end_datetime = datetime.datetime.combine(end_date, datetime.time())

    # Convert the dates to Unix timestamps
    unix_start_date = int(start_datetime.timestamp())
    unix_end_date = int(end_datetime.timestamp())

    #query
    chart = session.query(UserListening.track, func.count(UserListening.track)).filter(
        UserListening.timestamp >= unix_start_date,
        UserListening.timestamp <= unix_end_date
        ).group_by(UserListening.track).order_by(func.count(UserListening.track).desc()).limit(limit).all()
    
    #insert data in list
    tracks = []
    
    for track, count in chart:
        tracks.append({
            "name": track,
            "count": count
        })

    if chart is None:
        raise CarInfoNotFoundError
    
    else:
        return tracks
    
#function for chart.getTopArtists (for a given week, the charts)    
def get_chart_top_artists(session: Session, limit: int, year: int, week: int):

    # Get the date of the first day of the given year
    first_day = datetime.datetime(year, 1, 1).date()

    # Get the date of the first Monday of the year (week 1)
    first_monday = first_day + datetime.timedelta(days=(7 - first_day.weekday()))

    # Get the start date of the requested week
    start_date = first_monday + datetime.timedelta(weeks=(week - 1))
    start_datetime = datetime.datetime.combine(start_date, datetime.time())

    # Get the end date of the requested week
    end_date = start_date + datetime.timedelta(days=6)
    end_datetime = datetime.datetime.combine(end_date, datetime.time())

    # Convert the dates to Unix timestamps
    unix_start_date = int(start_datetime.timestamp())
    unix_end_date = int(end_datetime.timestamp())
    
    #query
    chart = session.query(UserListening.artist, func.count(UserListening.artist)).filter(
        UserListening.timestamp >= unix_start_date,
        UserListening.timestamp <= unix_end_date
    ).group_by(UserListening.artist).order_by(func.count(UserListening.artist).desc()).limit(limit).all()
    
    #insert data in list
    artists = []
    
    for artist, count in chart:
        artists.append({
            "name": artist,
            "count": count
        })

    if chart is None:
        raise CarInfoNotFoundError
    
    else:
        return artists
    
#function for user.getRecentlyActive
def get_recent_active_users(session: Session, _limit: int):

    recent_users = session.query(UserListening).order_by(UserListening.timestamp.desc()).group_by(UserListening.user).limit(_limit).all()
    
    users = []

    for user in recent_users:
        date = datetime.date.fromtimestamp(user.timestamp)
        users.append({
            "user": user.user,
            "date": date
        })

    
    if recent_users is None:
        raise CarInfoNotFoundError
    
    else:
        return users