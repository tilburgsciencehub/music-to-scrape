from database import db
from sqlalchemy import Column, String
from sqlalchemy.sql import text

# listening history table
class listening(db.Model):
    user = db.Column(db.String)
    date = db.Column(db.Date)
    timestamp = db.Column(db.String)
    artist_id = db.Column(db.String, db.ForeignKey('artists.ArtistID'))
    song_id = db.Column(db.String, db.ForeignKey('songs.SongID'))
    unique_id = db.Column(db.String, primary_key=True)

    artist = db.relationship('artists', backref='listenings')
    song = db.relationship('songs', backref='listenings')

# artists table
class artists(db.Model):
    ArtistID = db.Column(db.String, primary_key=True)
    ArtistName = db.Column(db.String)
    ArtistLocation = db.Column(db.String)
    featured = db.Column(db.String)

# users table
class users(db.Model):
    username = db.Column(db.String, primary_key=True)
    age = db.Column(db.Integer)
    country = db.Column(db.String)
    description = db.Column(db.String)

# songs table
class songs(db.Model):
    ArtistID = db.Column(db.String)
    ArtistName = db.Column(db.String)
    SongID = db.Column(db.String, primary_key=True)
    Danceability = db.Column(db.Float)
    Duration = db.Column(db.Numeric)
    KeySignature = db.Column(db.Integer)
    Tempo = db.Column(db.Numeric)
    TimeSignature = db.Column(db.Integer)
    Title = db.Column(db.String)
    Year = db.Column(db.Integer)