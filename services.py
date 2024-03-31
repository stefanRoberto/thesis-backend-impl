from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import models
import schemas


def create_artist(artist: schemas.ArtistCreate, session: Session):
    db_artist = models.Artist(**artist.dict())

    session.add(db_artist)
    session.commit()
    session.refresh(db_artist)

    artist_dict = jsonable_encoder(db_artist)

    return schemas.Artist(**artist_dict)


def find_artist(artist_id: int, session: Session):
    db_artist = session.query(models.Artist).filter(models.Artist.id == artist_id).first()

    return db_artist


def read_artist(artist_id: int, session: Session):
    db_artist = find_artist(artist_id, session)
    artist_dict = jsonable_encoder(db_artist)

    return schemas.Artist(**artist_dict)


def update_artist(artist_id: int, artist: schemas.ArtistUpdate, session: Session):
    db_artist = find_artist(artist_id, session)

    for key, value in artist.dict().items():
        setattr(db_artist, key, value)

    session.commit()
    session.refresh(db_artist)

    artist_dict = jsonable_encoder(db_artist)

    return schemas.Artist(**artist_dict)


def delete_artist(artist_id: int, session: Session):
    db_artist = find_artist(artist_id, session)

    session.delete(db_artist)
    session.commit()

    artist_dict = jsonable_encoder(db_artist)

    return schemas.Artist(**artist_dict)
