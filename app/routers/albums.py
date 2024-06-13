from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import database, schemas
from app.services import albums

router = APIRouter(prefix='/albums', tags=['albums'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_album(album: schemas.AlbumCreate, session: Session = Depends(database.get_database)):
    try:
        album = albums.create_album(album, session)
        return schemas.ResponseSchema(code=201, message="Album created successfully", data=album)
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Artist with id {album.artist_id} does not exist") from e
