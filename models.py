from sqlalchemy import Integer, Boolean, String, Text, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# TODO: Add database models

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(18))
    country = Column(String)
    bio = Column(String(1500))
    genre = Column(String)
    listeners = Column(Integer, default=0)

    albums = relationship('Album', back_populates='artist')

class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(25))
    release_date = Column(DateTime)
    artist_id = Column(Integer, ForeignKey('artists.id'))

    artist = relationship('Artist', back_populates='albums')
    tracks = relationship('Track', back_populates='album')

class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(25))
    album_id = Column(Integer, ForeignKey('albums.id'))
    duration = Column(Integer)
    plays = Column(Integer, default=0)

    album = relationship('Album', back_populates='tracks')

# TODO: Finish User model (add playlists)
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(18))
    username = Column(String(25), unique=True, index=True)
    email = Column(String(320), unique=True, index=True)
    password = Column(String)
