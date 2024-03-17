import datetime as dt

from sqlalchemy import Integer, Boolean, String, Text, Column, DateTime, ForeignKey, Table, UUID
from sqlalchemy.orm import relationship
from database import Base

playlist_track_association_table = Table(
    'playlist_track_association',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('track_id', Integer, ForeignKey('tracks.id'))
)


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(18))
    country = Column(String)
    birth_date = Column(DateTime, default=dt.datetime.utcnow())
    bio = Column(String(1500))
    genre = Column(String)
    listeners = Column(Integer, default=0)

    albums = relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(25))
    release_date = Column(DateTime, default=dt.datetime.utcnow())
    artist_id = Column(Integer, ForeignKey('artists.id'))

    artist = relationship('Artist', back_populates='albums')
    tracks = relationship('Track', back_populates='album')


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(25))
    album_id = Column(Integer, ForeignKey('albums.id'))
    duration = Column(Integer)
    plays = Column(Integer, default=0)
    release_date = Column(DateTime, default=dt.datetime.utcnow())

    album = relationship('Album', back_populates='tracks')
    playlists = relationship('Playlist', secondary=playlist_track_association_table, back_populates='tracks')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(18))
    username = Column(String(25), unique=True, index=True)
    email = Column(String(320), unique=True, index=True)
    password = Column(String)
    birth_date = Column(DateTime, default=dt.datetime.utcnow())

    playlists = relationship('Playlist', back_populates='user')


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(25))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=dt.datetime.utcnow())

    user = relationship('User', back_populates='playlists')
    tracks = relationship('Track', secondary=playlist_track_association_table, back_populates='playlists')
