import datetime
from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app import schemas
from app.main import app

client = TestClient(app)


@pytest.fixture
def session():
    return MagicMock(spec=Session)


@pytest.fixture(scope="module")
def artist_create_schema():
    return schemas.ArtistCreate(name="Test Artist",
                                country="UK",
                                birth_date=datetime.date.today(),
                                bio="Test bio",
                                genre="Test genre")


@pytest.fixture
def artist_update_schema():
    return schemas.ArtistUpdate(bio="Updated test bio",
                                genre="Updated test genre")


@pytest.fixture
def album_create_schema():
    return schemas.AlbumCreate(title="Test Album",
                               release_date=datetime.date.today(),
                               artist_id=1)


@pytest.fixture
def album_update_schema():
    return schemas.AlbumUpdate(title="Updated Test Album",
                               release_date=datetime.date(2000, 1, 1))
