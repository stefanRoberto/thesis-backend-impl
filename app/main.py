from fastapi import FastAPI

from . import database
from .routers import artists
app = FastAPI()

database.create_database()

app.include_router(artists.router, prefix='/api')
