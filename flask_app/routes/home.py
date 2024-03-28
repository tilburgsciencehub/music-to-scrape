from flask import render_template, Blueprint
from database import init_app, db
from models import listening, artists, songs
from sqlalchemy import func, desc
import time
import random
import requests

home_bp = Blueprint('home', __name__)

# Function to fetch avatar for a user
def fetch_avatar(username):
    api_url = f"https://api.multiavatar.com/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
      return response.content.decode('utf-8')
    else:
      return None

# route for home
@home_bp.route('/')
def index():
    # get current time stamp
    currunix = int(time.time())

    # recently played tracks query
    subquery = (
        db.session.query(listening.song_id, listening.timestamp)
        .filter(listening.timestamp <= currunix)
        .order_by(listening.timestamp.desc())
        .limit(10)
        .subquery()
    )

    recent_tracks = db.session.query(
        subquery.c.timestamp.label("timestamp"),
        songs.ArtistName,
        songs.Title,
        songs.SongID,
    ).join(songs, subquery.c.song_id == songs.SongID)

    recent_tracks = list(recent_tracks)

    # top 15
    subquery = (
        db.session.query(
            listening.song_id,
            func.count(listening.song_id).label('count'),
        )
        .group_by(listening.song_id)
        .subquery()
    )

    top_songs = (
        db.session.query(
            subquery.c.song_id,
            songs.Title,
            songs.ArtistName,
            songs.ArtistID,
            subquery.c.count,
            func.row_number().over(order_by=subquery.c.count.desc()).label('rank'),
        )
        .join(songs, subquery.c.song_id == songs.SongID)
        .order_by(subquery.c.count.desc())
        .limit(15)
    )

    top_songs = list(top_songs)

    # featured artists
    featured_artists = (
        artists.query.filter_by(featured='1').order_by(func.random()).limit(8).all()
    )

    featured_artists = list(featured_artists)

    # recent users
    subquery1 = (
        db.session.query(
            listening.user,
            func.max(listening.timestamp).label('max_timestamp'),
        )
        .filter(listening.timestamp <= currunix)
        .group_by(listening.user)
        .order_by(desc('max_timestamp'))
        .limit(6)
        .subquery()
    )

    # One user may have more than one listening events with the same timestamp.
    # Only keep one of them, to prevent this user from appearing in the list more
    # than once.
    subquery2 = (
        db.session.query(
            subquery1.c.user,
            func.max(listening.song_id).label('song_id'),
            subquery1.c.max_timestamp,
        )
        .filter(listening.timestamp == subquery1.c.max_timestamp)
        .filter(listening.user == subquery1.c.user)
        .group_by(subquery1.c.user, subquery1.c.max_timestamp)
        .subquery()
    )

    recent_users = (
        db.session.query(
            subquery2.c.user,
            subquery2.c.max_timestamp,
            songs.ArtistName,
            songs.Title,
        )
        .join(songs, subquery2.c.song_id == songs.SongID)
        .order_by(desc('max_timestamp'))
    )

    # make song information disappear
    recent_users_update = []
    cntr = 0
    for user in recent_users:
        cntr += 1
        user_dict = dict(zip(user.keys(), user))

        # Add the new data point to the dictionary
        if 1 <= cntr <= 5 and random.choice([True, False]):
            user_dict['show_song'] = False
        else:
            user_dict['show_song'] = True

        # Fetch avatar for the user
        user_dict['avatar'] = fetch_avatar(user_dict['user'])

        # Append the updated dictionary to the list
        recent_users_update.append(user_dict)

    # render template
    return render_template(
        'index.html',
        head='partials/head.html',
        loading='partials/loading.html',
        header='partials/header.html',
        footer='partials/footer.html',
        tracks=recent_tracks,
        top_songs=top_songs,
        featured_artists=featured_artists,
        recent_users=recent_users_update,
    )
