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
