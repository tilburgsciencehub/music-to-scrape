# crud.py
from typing import List
from sqlalchemy.orm import Session, aliased
from exceptions import CarInfoNotFoundError
from models import UserInfo, UserListening, Songs, Artists
from sqlalchemy import func, desc, and_
import time
import datetime
from datetime import timedelta


# Function to get list of users
def get_all_users(session: Session, limit: int, offset: int) -> List[UserInfo]:
    return session.query(UserInfo).offset(offset).limit(limit).all()

# Function to  get info of particular user
def get_user_info_by_username(session: Session, _username: str) -> UserInfo:
    user_info = session.query(UserInfo).get(_username)
    count_plays = session.query(
        UserListening).filter_by(user=_username).count()
    favorite_artist = session.query(UserListening.artist_id, func.count(UserListening.artist_id)).filter_by(
        user=_username).group_by(UserListening.artist_id).order_by(func.count(UserListening.artist_id).desc()).first()
    user_info2 = user_info.__dict__
    artist_name = str(favorite_artist[0])
    favorite_artist_name = session.query(
        Artists.ArtistName).filter_by(ArtistID=artist_name)

    user_dict = {'user_info': user_info2, 'total_plays': count_plays,
                 'favourite_artist': str(favorite_artist_name[0][0])}

    if user_dict is None:
        raise CarInfoNotFoundError

    return user_dict

# Function to get total user plays
def count_plays_by_username(session: Session, _username: str) -> UserListening:
    count_plays = session.query(
        UserListening).filter_by(user=_username).count()

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

    for i in range(0, _limit):

        artist = recent_tracks[i].artist
        track = recent_tracks[i].song

        tracks.append({
            "artist": artist.ArtistName,
            "track": track.title,
            "timestamp": recent_tracks[i].timestamp
        })

    if recent_tracks is None:
        raise CarInfoNotFoundError

    else:
        return tracks

# Function for user.GetTopArtists
def get_top_artists_for_user(session: Session, username: str, limit: int = 5, period: str = "overall"):

    # get period
    if (period == "overall"):
        end = 2000000000
        start = 0

    elif (period == "7day"):
        end = int(time.time())
        start = end - (7 * 24 * 60 * 60)

    elif (period == "1month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=30)).timestamp())

    elif (period == "3month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=90)).timestamp())

    elif (period == "6month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=180)).timestamp())

    elif (period == "12month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=365)).timestamp())

    # query
    top_artists = session.query(UserListening.artist_id, func.count(UserListening.artist_id)).filter(
        UserListening.user == username,
        UserListening.timestamp >= start,
        UserListening.timestamp <= end).group_by(UserListening.artist_id).order_by(func.count(UserListening.artist_id).desc()).limit(limit).all()

    # insert data in list
    artists = []

    for artistid, count in top_artists:
        favorite_artist_name = session.query(
            Artists.ArtistName).filter_by(ArtistID=artistid).first()

        artists.append({
            "name": favorite_artist_name[0],
            "count": count
        })

    if top_artists is None:
        raise CarInfoNotFoundError

    else:
        return artists

# Function for user.GetTopTracks  7day | 1month | 3month | 6month | 12month
def get_top_tracks_for_user(session: Session, username: str, limit: int = 5, period: str = "overall"):

    # get period
    if (period == "overall"):
        end = 2000000000
        start = 0

    elif (period == "7day"):
        end = int(time.time())
        start = end - (7 * 24 * 60 * 60)

    elif (period == "1month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=30)).timestamp())

    elif (period == "3month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=90)).timestamp())

    elif (period == "6month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=180)).timestamp())

    elif (period == "12month"):
        end = int(time.time())
        start = int((datetime.now() - timedelta(days=365)).timestamp())

    # query
    top_tracks = session.query(UserListening.song_id, func.count(UserListening.song_id)).filter(
        UserListening.user == username,
        UserListening.timestamp >= start,
        UserListening.timestamp <= end).group_by(UserListening.song_id).order_by(func.count(UserListening.song_id).desc()).limit(limit).all()

    # insert data in list
    tracks = []

    for track, count in top_tracks:

        favorite_track_name = session.query(
            Songs.title).filter_by(songid=track).first()

        tracks.append({
            "name": favorite_track_name[0],
            "count": count
        })

    if top_tracks is None:
        raise CarInfoNotFoundError

    else:
        return tracks

# Function fur user.GetWeeklyTrackChart
def get_weekly_track_chart_for_user(session: Session, username: str):
    # get the last week's date range
    last_week_start = (datetime.datetime.now() -
                       datetime.timedelta(days=7)).timestamp()
    last_week_end = (datetime.datetime.now()).timestamp()

    # get the user's plays from the last week
    plays = session.query(UserListening).filter(
        UserListening.user == username,
        UserListening.timestamp >= last_week_start,
        UserListening.timestamp <= last_week_end,
    ).all()

    # group plays by track
    track_plays = {}
    for play in plays:
        track = play.song_id
        if track in track_plays:
            track_plays[track] += 1
        else:
            track_plays[track] = 1

    # sort tracks by play count and get the top 10
    top_tracks = sorted(track_plays.items(),
                        key=lambda x: x[1], reverse=True)[:10]

    # get the track details for the top tracks
    track_details = []
    for track_name, play_count in top_tracks:
        track_dets = session.query(Songs.artistname, Songs.title).filter_by(
            songid=track_name).first()
        track_details.append({
            "name": track_dets[1],
            "artist": track_dets[0],
            "play_count": play_count
        })

    return track_details

# Function fur user.GetWeeklyTrackChart
def get_weekly_artist_chart_for_user(session: Session, username: str, limit: int):
    # get the last week's date range
    last_week_start = (datetime.datetime.now() -
                       datetime.timedelta(days=7)).timestamp()
    last_week_end = (datetime.datetime.now()).timestamp()

    # get the user's plays from the last week
    plays = session.query(UserListening).filter(
        UserListening.user == username,
        UserListening.timestamp >= last_week_start,
        UserListening.timestamp <= last_week_end,
    ).all()

    # group plays by track
    artist_plays = {}
    for play in plays:
        artist = play.artist_id
        if artist in artist_plays:
            artist_plays[artist] += 1
        else:
            artist_plays[artist] = 1

    # sort artists by play count and get the top 10
    top_artists = sorted(artist_plays.items(),
                         key=lambda x: x[1], reverse=True)[:limit]

    # get the track details for the top tracks
    artist_details = []
    for artist, play_count in top_artists:
        artist_name = session.query(
            Artists.ArtistName).filter_by(ArtistID=artist).first()
        artist_details.append({
            "artist": artist_name[0],
            "play_count": play_count
        })

    return artist_details

# Function for artist.GetTopTracks
def get_top_tracks_for_artist(session: Session, artist: str, limit: int = 5):

    # replace _ with space
    if "_" in artist:
        artist_name = artist.replace("_", " ")

    else:
        artist_name = artist

    # query for fetching artist_id
    artist_id_query = session.query(Artists.ArtistID).filter(
        Artists.ArtistName == artist_name).first()

    artist_id = str(artist_id_query[0])

    # query
    top_tracks = session.query(UserListening.song_id, func.count(UserListening.song_id)).filter(
        UserListening.artist_id == artist_id).group_by(UserListening.song_id).order_by(func.count(UserListening.song_id).desc()).limit(limit).all()

    # insert data in list
    tracks = []

    for trackid, count in top_tracks:
        track_name = session.query(Songs.title).filter(
            Songs.songid == trackid).first()
        tracks.append({
            "name": track_name[0],
            "count": count
        })

    if top_tracks is None:
        raise CarInfoNotFoundError

    else:
        return tracks

# function for chart.getTopTracks (for a given unixtimestamp, the charts)
def get_chart_top_tracks(session: Session, limit: int, 
                         unixtimestamp: int = None):
    currtime = int(time.time())
    
    if unixtimestamp is None: unixtimestamp = currtime
    if unixtimestamp > currtime: unixtimestamp = currtime

    # Convert the dates to Unix timestamps
    unix_start_date = unixtimestamp
    unix_end_date = max(unixtimestamp + 24 * 3600 * 7, currtime)

    # query
    chart = session.query(UserListening.song_id, func.count(UserListening.song_id)).filter(
        UserListening.timestamp >= unix_start_date,
        UserListening.timestamp <= unix_end_date
    ).group_by(UserListening.song_id).order_by(func.count(UserListening.song_id).desc()).limit(limit).all()

    # insert data in list
    tracks = []

    for track_id, count in chart:
        track_query = session.query(Songs.title, Songs.artistname).filter(
            Songs.songid == track_id).first()
        track = track_query[0]
        artist = track_query[1]

        tracks.append({
            "name": track,
            "artist": artist,
            "plays": count
        })

    if chart is None:
        raise CarInfoNotFoundError

    else:
        return {'tracks':tracks, 'unix_start':unix_start_date, 'unix_end': unix_end_date}

# function for chart.getTopArtists (for a given week, the charts)
def get_chart_top_artists(session: Session, limit: int, unixtimestamp: int = None):

    currtime = int(time.time())
    
    if unixtimestamp is None: unixtimestamp = currtime
    if unixtimestamp > currtime: unixtimestamp = currtime

    # Convert the dates to Unix timestamps
    unix_start_date = unixtimestamp
    unix_end_date = max(unixtimestamp + 24 * 3600 * 7, currtime)

    # query
    chart = session.query(UserListening.artist_id, func.count(UserListening.artist_id)).filter(
        UserListening.timestamp >= unix_start_date,
        UserListening.timestamp <= unix_end_date
    ).group_by(UserListening.artist_id).order_by(func.count(UserListening.artist_id).desc()).limit(limit).all()

    # insert data in list
    artists = []

    for artist, count in chart:
        artist_query = session.query(Artists.ArtistName).filter(
            Artists.ArtistID == artist).first()
        artist_name = artist_query[0]
        artists.append({
            "name": artist_name,
            "plays": count
        })

    if chart is None:
        raise CarInfoNotFoundError

    else:
        return {'artists':artists, 'unix_start':unix_start_date, 'unix_end': unix_end_date}

# function for user.getRecentlyActive
def get_recent_active_users(session: Session, _limit: int):
    subquery = session.query(UserListening.user, func.max(UserListening.timestamp).label("max_timestamp")) \
        .group_by(UserListening.user) \
        .subquery()

    recent_users = session.query(UserListening.user, UserListening.timestamp) \
        .join(subquery, and_(UserListening.user == subquery.c.user, UserListening.timestamp == subquery.c.max_timestamp)) \
        .order_by(desc(UserListening.timestamp)) \
        .limit(_limit) \
        .all()

    users = []

    for user, timestamp in recent_users:
        date = datetime.date.fromtimestamp(float(timestamp))
        users.append({
            "user": user,
            "date": date
        })

    if not users:
        raise CarInfoNotFoundError

    return users

# function for artist.featured
def get_featured_artists(session: Session, _limit: int):

    featured_artists = session.query(Artists.ArtistName, Artists.featured, Artists.ArtistID).\
        filter(Artists.featured == '1').\
        order_by(func.random()).\
        limit(_limit).\
        all()

    artists = []

    for artist in featured_artists:

        artists.append({
            "artist": artist[0],
            "artist_id": artist[2],
            "featured": 'TRUE'
        })
    
    if featured_artists is None:

        raise CarInfoNotFoundError

    else:
        return artists
    
# function for artist.getInfo
def get_artist_info(session: Session,artistid: str):
    today = datetime.datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_date_unix = int(start_of_week.timestamp())
    end_date_unix = int(end_of_week.timestamp())

    # replace _ with space
    if "_" in artistid:
        artistid = artistid.replace("_", " ")

    else:
        pass

    artist_info = session.query(Artists.ArtistID, Artists.ArtistName, Artists.featured, Artists.artistlocation).filter(Artists.ArtistID == artistid).first()

    artist_name = artist_info[1]
    count_plays = session.query(
        UserListening).filter_by(artist_id = artistid).count()

    count_songs = session.query(
        Songs).filter_by(artistid = artistid).count()
    
    count_plays_last_week = session.query(UserListening).filter_by(artist_id=artistid).filter(UserListening.timestamp >= start_date_unix, UserListening.timestamp <= end_date_unix).count()

    top_songs = session.query(UserListening.song_id, Songs.title, func.count(UserListening.song_id).label('plays')).\
        filter(UserListening.artist_id == artistid).\
        join(UserListening.song).\
        group_by(UserListening.song_id).\
        order_by(desc('plays')).\
        limit(5).all()
    
    top_songs_list = []

    for song in top_songs:

        song_dict = {}

        song_dict['title'] = song[1]
        song_dict['plays'] = song[2]

        top_songs_list.append(song_dict)
    
    artists = {}

    artists['artistid'] = artist_info[0]
    artists['artistname'] = artist_info[1]
    artists['artistfeatured'] = artist_info[2]
    artists['total_songs'] = count_songs
    artists['top_songs'] = top_songs_list

    if (artist_info[3] is None):
        artists['artistlocation'] = str('Not Set')
    
    else:
        artists['artistlocation'] = artist_info[3]
    
    artists['total_plays'] = count_plays
    artists['plays_last_week'] = count_plays_last_week

    if artist_info is None:
        raise CarInfoNotFoundError

    else:
        return artists
