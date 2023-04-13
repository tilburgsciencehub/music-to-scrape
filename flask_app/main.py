from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text
import os

#initialize Flask App & Database
app = Flask(__name__)

# get absolute path to Flask app file
app_dir = os.path.abspath(os.path.dirname(__file__))

# construct path to database file
db_path = os.path.join(app_dir, 'apistoscrape.db')

# set database URI in Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)

#create classes for database tables

#table listening
class listening(db.Model):
    user = db.Column(db.String(10))
    date = db.Column(db.Date)
    timestamp = db.Column(db.String(16))
    artist_id = db.Column(db.String(18), db.ForeignKey('artists.ArtistID'))
    song_id = db.Column(db.String(18), db.ForeignKey('songs.SongID'))
    unique_id = db.Column(db.String(52), primary_key=True)

    artist = db.relationship('artists', backref='listenings')
    song = db.relationship('songs', backref='listenings')

class artists(db.Model):
    ArtistID = db.Column(db.String(18), primary_key=True)
    ArtistName = db.Column(db.String(400))
    ArtistLocation = db.Column(db.String(200))
    featured = db.Column(db.String(5))

class users(db.Model):
    username = db.Column(db.String(18), primary_key=True)
    age = db.Column(db.Integer)
    country = db.Column(db.String(2))
    description = db.Column(db.String(500))

class songs(db.Model):
    ArtistID = db.Column(db.String(20))
    ArtistName = db.Column(db.String(400))
    SongID = db.Column(db.String(20), primary_key=True)
    ArtistID = db.Column(db.Integer)
    Danceability = db.Column(db.Numeric(1,0))
    Duration = db.Column(db.Numeric(15,5))
    KeySignature = db.Column(db.Integer)
    Tempo = db.Column(db.Numeric(20,3))
    TimeSignature = db.Column(db.Integer)
    Title = db.Column(db.String(400))
    Year = db.Column(db.Integer)

@app.route('/')
def index():

    #recent tracks query
    recent_tracks = db.session.query(listening.timestamp, songs.ArtistName, songs.Title)\
                .join(songs, listening.song_id == songs.SongID)\
                .order_by(listening.timestamp.desc())\
                .limit(10)\
                .all()
    
    #weekly top 15
    top_songs = db.session.query(listening.song_id, songs.Title, songs.ArtistName, 
                    func.count(listening.song_id), 
                    func.row_number().over(order_by=func.count(listening.song_id).desc()).label('rank'))\
            .join(songs, listening.song_id == songs.SongID)\
            .group_by(listening.song_id)\
            .order_by(func.count(listening.song_id).desc())\
            .limit(15)\
            .all()
    
    #featured artists
    featured_artists = artists.query.filter_by(featured='TRUE').order_by(func.random()).limit(8).all()

    #recent users
    recent_users = db.session.query(listening.timestamp, listening.user, songs.ArtistName, songs.Title)\
                .join(songs, listening.song_id == songs.SongID)\
                .group_by(listening.user)\
                .order_by(listening.timestamp.desc())\
                .limit(6)\
                .all()
    #render template
    return render_template('index.html', tracks = recent_tracks, top_songs = top_songs, featured_artists = featured_artists, recent_users = recent_users)

@app.route('/artist')
def artist_page():
    return render_template('artist_page.html')

@app.route('/user')
def user_page():
    return render_template('user_page.html')

@app.route('/search-results')
def search_results():
    return render_template('search_results.html')

# Add a static route for CSS
@app.route('/static/css/<path:path>')
def static_css(path):
    return app.send_static_file('css/' + path)

if __name__ == '__main__':
    app.run(debug=True)
