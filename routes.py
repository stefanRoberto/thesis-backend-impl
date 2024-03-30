from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import UnmappedInstanceError

import database
import services
from schemas import *

router = APIRouter()


@router.post('/artists/', status_code=status.HTTP_201_CREATED)
def create_artist(artist: ArtistCreate, session: Session = Depends(database.get_database)):
    artist = services.create_artist(artist, session)
    return ResponseSchema(code=201, message="Artist created successfully", data=artist)


@router.get('/artists/{artist_id}')
def read_artist(artist_id: int, session: Session = Depends(database.get_database)):
    try:
        artist = services.read_artist(artist_id, session)
        return ResponseSchema(code=200, message="Artist retrieved successfully", data=artist)
    except TypeError as e:
        raise HTTPException(status_code=404, detail="Artist not found") from e


@router.patch('/artists/{artist_id}')
def update_artist(artist_id: int, artist: ArtistUpdate, session: Session = Depends(database.get_database)):
    try:
        artist = services.update_artist(artist_id, artist, session)
        return ResponseSchema(code=200, message="Artist updated successfully", data=artist)
    except (TypeError, AttributeError) as e:
        raise HTTPException(status_code=404, detail="Artist not found") from e


@router.delete('/artists/{artist_id}')
def delete_artist(artist_id: int, session: Session = Depends(database.get_database)):
    try:
        artist = services.delete_artist(artist_id, session)
        return ResponseSchema(code=200, message="Artist deleted successfully", data=artist)
    except UnmappedInstanceError as e:
        raise HTTPException(status_code=404, detail="Artist not found") from e
