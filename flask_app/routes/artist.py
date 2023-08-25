from flask import render_template, request, Blueprint
from database import init_app, db
from models import listening, artists, songs, users
import time

artist_bp = Blueprint('artist', __name__)

# route for artist
@artist_bp.route('/artist')
def artist_page():

    # get artist id parameter
    artist_id = request.args.get('artist-id')

    # get current time stamp
    currunix = int(time.time())

    # get artist info
    artist_info = artists.query.filter_by(ArtistID=artist_id).first()

    # count number of plays
    num_plays = listening.query.filter_by(artist_id=artist_id).filter(listening.timestamp <= currunix).count()
    
    # top 10 songs for artist
    top_songs = db.session.query(
        db.func.row_number().over(order_by=db.func.count(
            listening.song_id).desc()).label('rank'),
        listening.song_id,
        db.func.count(listening.song_id).label('count'),
        songs.Title
    ).\
        join(songs, listening.song_id == songs.SongID).\
        filter(listening.artist_id == artist_id).\
        filter(listening.timestamp <= currunix).\
        group_by(listening.song_id).\
        order_by(db.func.count(listening.song_id).desc()).\
        limit(10).all()

    # render template
    return render_template('artist_page.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html', artist_id=artist_id, artist_info=artist_info, num_plays=num_plays, top_songs=top_songs)
