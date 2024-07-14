from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

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


@router.get('/{album_id}', responses={404: {"description": "Not found"}})
def read_album(album_id: int, session: Session = Depends(database.get_database)):
    try:
        album = albums.read_album(album_id, session)
        return schemas.ResponseSchema(code=200, message="Album retrieved successfully", data=album)
    except TypeError as e:
        raise HTTPException(status_code=404, detail="Album not found") from e


@router.patch('/{album_id}', responses={404: {"description": "Not found"}})
def update_album(album_id: int, album: schemas.AlbumUpdate, session: Session = Depends(database.get_database)):
    try:
        album = albums.update_album(album_id, album, session)
        return schemas.ResponseSchema(code=200, message="Album updated successfully", data=album)
    except (TypeError, AttributeError) as e:
        raise HTTPException(status_code=404, detail="Album not found") from e


@router.delete('/{album_id}', responses={404: {"description": "Not found"}})
def delete_album(album_id: int, session: Session = Depends(database.get_database)):
    try:
        album = albums.delete_album(album_id, session)
        return schemas.ResponseSchema(code=200, message="Album deleted successfully", data=album)
    except UnmappedInstanceError as e:
        raise HTTPException(status_code=404, detail="Album not found") from e
