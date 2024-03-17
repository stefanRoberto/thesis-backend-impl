import datetime as dt
from typing import Optional

from pydantic import BaseModel

class ArtistBase(BaseModel):
    name: str
    country: str
    birth_date: dt.datetime
    bio: Optional[str]
    genre: str

class ArtistCreate(ArtistBase):
    pass

class Artist(ArtistBase):
    id: int
    listeners: int = 0

    class Config:
        orm_mode = True

# TODO: Add pydantic schemas for each SQLAlchemy model