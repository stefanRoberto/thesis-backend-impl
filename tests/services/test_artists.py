import datetime

import pytest
from unittest.mock import MagicMock, ANY

from app import models, schemas
from app.services import artists


@pytest.fixture
def db_artist():
    return models.Artist(
        id=1,
        name="Test Artist",
        country="UK",
        birth_date=datetime.date.today(),
        bio="Test bio",
        genre="Test genre",
        listeners=0
    )


@pytest.fixture
def find_artist_mock(db_artist):
    return MagicMock(return_value=db_artist)


@pytest.fixture
def jsonable_encoder_mock():
    return MagicMock(return_value={"id": 1,
                                   "name": "Test Artist",
                                   "country": "UK",
                                   "birth_date": datetime.date.today().isoformat(),
                                   "bio": "Test bio",
                                   "genre": "Test genre",
                                   "listeners": 0})


@pytest.fixture
def jsonable_encoder_mock_updated():
    return MagicMock(return_value={"id": 1,
                                   "name": "Test Artist",
                                   "country": "UK",
                                   "birth_date": datetime.date.today().isoformat(),
                                   "bio": "Updated test bio",
                                   "genre": "Updated test genre",
                                   "listeners": 0})


@pytest.fixture
def query_mock(db_artist):
    query_mock = MagicMock()
    query_mock.filter().first.return_value = db_artist

    return query_mock


def test_create_artist(session, artist_create_schema, jsonable_encoder_mock):
    artists.jsonable_encoder = jsonable_encoder_mock

    created_artist = artists.create_artist(artist_create_schema, session)

    session.add.assert_called_once_with(ANY)
    assert isinstance(session.add.call_args.args[0], models.Artist)

    session.commit.assert_called_once()

    session.refresh.assert_called_once_with(ANY)
    assert isinstance(session.refresh.call_args.args[0], models.Artist)

    artists.jsonable_encoder.assert_called_once_with(ANY)

    assert isinstance(created_artist, schemas.Artist)
    assert created_artist.id == 1
    assert created_artist.name == "Test Artist"
    assert created_artist.country == "UK"
    assert created_artist.birth_date == datetime.date.today()
    assert created_artist.bio == "Test bio"
    assert created_artist.genre == "Test genre"
    assert created_artist.listeners == 0


def test_find_artist(session, db_artist, query_mock):
    session.query.return_value = query_mock

    found_artist = artists.find_artist(1, session)

    session.query().filter().first.assert_called_once()

    assert isinstance(found_artist, models.Artist)
    assert found_artist == db_artist


def test_read_artist(session, db_artist, find_artist_mock, jsonable_encoder_mock):
    artists.find_artist = find_artist_mock
    artists.jsonable_encoder = jsonable_encoder_mock

    read_artist = artists.read_artist(1, session)

    artists.find_artist.assert_called_once_with(1, session)
    artists.jsonable_encoder.assert_called_once_with(db_artist)

    assert isinstance(read_artist, schemas.Artist)
    assert read_artist.id == 1
    assert read_artist.name == "Test Artist"
    assert read_artist.country == "UK"
    assert read_artist.birth_date == datetime.date.today()
    assert read_artist.bio == "Test bio"
    assert read_artist.genre == "Test genre"
    assert read_artist.listeners == 0


def test_update_artist(session, db_artist, find_artist_mock, jsonable_encoder_mock_updated, artist_update_schema):
    artists.find_artist = find_artist_mock
    session.commit.return_value = None
    session.refresh.return_value = None
    artists.jsonable_encoder = jsonable_encoder_mock_updated

    updated_artist = artists.update_artist(1,
                                           artist_update_schema,
                                           session)

    artists.find_artist.assert_called_once_with(1, session)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(db_artist)
    artists.jsonable_encoder.assert_called_once_with(db_artist)

    assert isinstance(updated_artist, schemas.Artist)
    assert updated_artist.id == 1
    assert updated_artist.name == "Test Artist"
    assert updated_artist.country == "UK"
    assert updated_artist.birth_date == datetime.date.today()
    assert updated_artist.bio == "Updated test bio"
    assert updated_artist.genre == "Updated test genre"
    assert updated_artist.listeners == 0


def test_delete_artist(session, db_artist, find_artist_mock, jsonable_encoder_mock):
    artists.find_artist = find_artist_mock
    session.commit.return_value = None
    artists.jsonable_encoder = jsonable_encoder_mock

    deleted_artist = artists.delete_artist(1, session)

    artists.find_artist.assert_called_once_with(1, session)
    session.delete.assert_called_once_with(db_artist)
    session.commit.assert_called_once()
    artists.jsonable_encoder.assert_called_once_with(db_artist)

    assert isinstance(deleted_artist, schemas.Artist)
    assert deleted_artist.id == 1
    assert deleted_artist.name == "Test Artist"
    assert deleted_artist.country == "UK"
    assert deleted_artist.birth_date == datetime.date.today()
    assert deleted_artist.bio == "Test bio"
    assert deleted_artist.genre == "Test genre"
    assert deleted_artist.listeners == 0
