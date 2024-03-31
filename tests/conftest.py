import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

import database
from main import app
from schemas import *

client = TestClient(app)

database.drop_database()
database.create_database()


@pytest.fixture
def session():
    return MagicMock(spec=Session)


@pytest.fixture
def artist_create_schema():
    return ArtistCreate(name="Test Artist",
                        country="UK",
                        birth_date=datetime.date.today(),
                        bio="Test bio",
                        genre="Test genre")


@pytest.fixture
def artist_update_schema():
    return ArtistUpdate(bio="Updated test bio",
                        genre="Updated test genre")
