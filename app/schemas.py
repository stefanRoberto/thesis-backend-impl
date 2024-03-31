import datetime as dt
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, Field, EmailStr


class ArtistBase(BaseModel):
    name: str = Field(min_length=1, max_length=18)
    country: str = Field(min_length=2, max_length=2)
    birth_date: dt.date = Field(default_factory=dt.date.today)
    bio: Optional[str] = Field(max_length=1500)
    genre: str = Field(min_length=1, max_length=25)


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    bio: Optional[str] = Field(max_length=1500)
    genre: Optional[str] = Field(min_length=1, max_length=25)


class Artist(ArtistBase):
    id: int
    listeners: int = 0


class AlbumBase(BaseModel):
    title: str = Field(min_length=1, max_length=25)
    release_date: dt.date = Field(default_factory=dt.date.today)
    artist_id: int = Field(ge=1)


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=25)
    release_date: Optional[dt.date] = Field(default_factory=dt.date.today)


class Album(AlbumBase):
    id: int


class TrackBase(BaseModel):
    title: str = Field(min_length=1, max_length=25)
    album_id: int = Field(ge=1)
    duration: int = Field(ge=1)
    release_date: dt.date = Field(default_factory=dt.date.today)


class TrackCreate(TrackBase):
    pass


class TrackUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=25)
    release_date: Optional[dt.date] = Field(default_factory=dt.date.today)


class Track(TrackBase):
    id: int
    plays: int = 0


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=25)


class UserCreate(UserBase):
    username: str = Field(min_length=1, max_length=25, unique=True)
    password: str = Field(min_length=8)
    email: EmailStr = Field(min_length=6, max_length=320, unique=True)
    birth_date: dt.date = Field(default_factory=dt.date.today)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=25)


class User(UserBase):
    id: int


class PlaylistBase(BaseModel):
    title: str = Field(min_length=1, max_length=25)
    user_id: int = Field(ge=1)


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(BaseModel):
    title: Optional[str] = Field(min_length=1, max_length=25)


class Playlist(PlaylistBase):
    id: int
    created_at: dt.date = Field(default_factory=dt.date.today)


class PlaylistTrackAssociationBase(BaseModel):
    playlist_id: int = Field(ge=1)
    track_id: int = Field(ge=1)


class PlaylistTrackAssociationCreate(PlaylistTrackAssociationBase):
    pass


class PlaylistTrackAssociation(PlaylistTrackAssociationBase):
    pass


DataT = TypeVar('DataT')


class ResponseSchema(BaseModel, Generic[DataT]):
    code: int
    message: str
    data: Optional[DataT]
