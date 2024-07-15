from fastapi import FastAPI

from . import database
from .routers import artists, albums

app = FastAPI()

database.create_database()

app.include_router(artists.router, prefix='/api')
app.include_router(albums.router, prefix='/api')
