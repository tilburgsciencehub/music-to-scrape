from flask import render_template, Blueprint
from database import init_app, db
from models import listening, artists, songs
from sqlalchemy import func, desc

home_bp = Blueprint('home', __name__)

# route for home
@home_bp.route('/')
def index():

    # recent tracks query
    subquery = db.session.query(
        listening.song_id,
        listening.timestamp
    ).order_by(listening.timestamp.desc()).limit(10).subquery()

    recent_tracks = db.session.query(
        subquery.c.timestamp,
        songs.ArtistName,
        songs.Title,
        songs.SongID
    ).join(songs, subquery.c.song_id == songs.SongID)

    # top 15
    top_songs = db.session.query(listening.song_id, songs.Title, songs.ArtistName, songs.ArtistID,
                                 func.count(listening.song_id),
                                 func.row_number().over(order_by=func.count(listening.song_id).desc()).label('rank'))\
        .join(songs, listening.song_id == songs.SongID)\
        .group_by(listening.song_id)\
        .order_by(func.count(listening.song_id).desc())\
        .limit(15)

    # featured artists
    featured_artists = artists.query.filter_by(
        featured='1').order_by(func.random()).limit(8).all()

    # recent users
    recent_users = db.session.query(
        listening.user,
        func.max(listening.timestamp).label("max_timestamp"),
        songs.ArtistName,
        songs.Title
    ).join(listening.song).group_by(listening.user).order_by(desc("max_timestamp")).limit(6)

    # render template
    return render_template('index.html', head='partials/head.html', loading='partials/loading.html', header='partials/header.html', footer='partials/footer.html', tracks=recent_tracks, top_songs=top_songs, featured_artists=featured_artists, recent_users=recent_users)
