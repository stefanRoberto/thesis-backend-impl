from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

from app import database, schemas
from app.services import artists

router = APIRouter(prefix='/artists', tags=['artists'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_artist(artist: schemas.ArtistCreate, session: Session = Depends(database.get_database)):
    artist = artists.create_artist(artist, session)
    return schemas.ResponseSchema(code=201, message="Artist created successfully", data=artist)


@router.get('/{artist_id}', responses={404: {"description": "Not found"}})
def read_artist(artist_id: int, session: Session = Depends(database.get_database)):
    try:
        artist = artists.read_artist(artist_id, session)
        return schemas.ResponseSchema(code=200, message="Artist retrieved successfully", data=artist)
    except TypeError as e:
        raise HTTPException(status_code=404, detail="Artist not found") from e


@router.patch('/{artist_id}', responses={404: {"description": "Not found"}})
def update_artist(artist_id: int, artist: schemas.ArtistUpdate, session: Session = Depends(database.get_database)):
    try:
        artist = artists.update_artist(artist_id, artist, session)
        return schemas.ResponseSchema(code=200, message="Artist updated successfully", data=artist)
    except (TypeError, AttributeError) as e:
        raise HTTPException(status_code=404, detail="Artist not found") from e


@router.delete('/{artist_id}', responses={404: {"description": "Not found"}})
def delete_artist(artist_id: int, session: Session = Depends(database.get_database)):
    try:
        artist = artists.delete_artist(artist_id, session)
        return schemas.ResponseSchema(code=200, message="Artist deleted successfully", data=artist)
    except UnmappedInstanceError as e:
        raise HTTPException(status_code=404, detail="Artist not found") from e
