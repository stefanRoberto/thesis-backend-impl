from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, schemas


def create_album(album: schemas.AlbumCreate, session: Session):
    db_album = models.Album(**album.dict())

    session.add(db_album)
    session.commit()
    session.refresh(db_album)

    album_dict = jsonable_encoder(db_album)

    return schemas.Album(**album_dict)


def find_album(album_id: int, session: Session):
    db_album = session.query(models.Album).filter(models.Album.id == album_id).first()

    return db_album


def read_album(album_id: int, session: Session):
    db_album = find_album(album_id, session)
    album_dict = jsonable_encoder(db_album)

    return schemas.Album(**album_dict)


def update_album(album_id: int, album: schemas.AlbumUpdate, session: Session):
    db_album = find_album(album_id, session)

    for key, value in album.dict().items():
        setattr(db_album, key, value)

    session.commit()
    session.refresh(db_album)

    album_dict = jsonable_encoder(db_album)

    return schemas.Album(**album_dict)


def delete_album(album_id: int, session: Session):
    db_album = find_album(album_id, session)

    session.delete(db_album)
    session.commit()

    album_dict = jsonable_encoder(db_album)

    return schemas.Album(**album_dict)
