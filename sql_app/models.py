from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Float
from sqlalchemy.orm import relationship
from database import Base

class UserInfo(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    age = Column(Integer)
    country = Column(String)
    description = Column(String)

    usersinfo = relationship("UserListening", back_populates="user_info")

class UserListening(Base):
    __tablename__ = "listening"

    user = Column(String, ForeignKey("users.username"))
    date = Column(String)
    timestamp = Column(Float)
    artist_id = Column(String, ForeignKey("artists.ArtistID"))
    song_id = Column(String, ForeignKey("songs.songid"))
    unique_id = Column(Integer, primary_key=True)

    # Relationship with UserInfo table
    user_info = relationship("UserInfo", back_populates="usersinfo")

    # Relationship with Artists table
    artist = relationship("Artists", back_populates="user_listenings")

    # Relationship with Songs table
    song = relationship("Songs", back_populates="user_songs")

class Artists(Base):
    __tablename__ = "artists"

    ArtistID = Column(String, primary_key=True)
    ArtistName = Column(String)
    artistlocation = Column(String)
    featured = Column(String)

    # Relationship with UserListening table
    user_listenings = relationship("UserListening", back_populates="artist")

class Songs(Base):
    __tablename__ = "songs"

    artistid = Column(String, ForeignKey("artists.artistid"))
    artistname = Column(String)
    songid = Column(String, primary_key=True)
    albumid = Column(Integer)
    danceability = Column(Numeric(1,0))
    duration = Column(Numeric(15,5))
    keysignature = Column(Integer)
    tempo = Column(Numeric(20,3))
    timesignature = Column(Integer)
    title = Column(String)

    # Relationship with UserListening table
    user_songs = relationship("UserListening", back_populates="song")
