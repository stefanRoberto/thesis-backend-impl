import datetime
from unittest.mock import MagicMock, ANY

import pytest

from app import models, schemas
from app.services import albums


@pytest.fixture
def db_album():
    return models.Album(
        id=1,
        title="Test Album",
        release_date=datetime.date.today(),
        artist_id=1
    )


@pytest.fixture
def find_album_mock(db_album):
    return MagicMock(return_value=db_album)


@pytest.fixture
def jsonable_encoder_mock():
    return MagicMock(return_value={"id": 1,
                                   "title": "Test Album",
                                   "release_date": datetime.date.today().isoformat(),
                                   "artist_id": 1})


@pytest.fixture
def jsonable_encoder_mock_updated():
    return MagicMock(return_value={"id": 1,
                                   "title": "Updated Test Album",
                                   "release_date": datetime.date(2000, 1, 1).isoformat(),
                                   "artist_id": 1})


@pytest.fixture
def query_mock(db_album):
    query_mock = MagicMock()
    query_mock.filter().first.return_value = db_album

    return query_mock


def test_create_album(session, album_create_schema, jsonable_encoder_mock):
    albums.jsonable_encoder = jsonable_encoder_mock

    created_album = albums.create_album(album_create_schema, session)

    session.add.assert_called_once_with(ANY)
    assert isinstance(session.add.call_args.args[0], models.Album)

    session.commit.assert_called_once()

    session.refresh.assert_called_once_with(ANY)

    albums.jsonable_encoder.assert_called_once_with(ANY)

    assert isinstance(created_album, schemas.Album)
    assert created_album.title == "Test Album"
    assert created_album.release_date == datetime.date.today()
    assert created_album.artist_id == 1


def test_find_album(session, db_album, query_mock):
    session.query.return_value = query_mock

    found_album = albums.find_album(1, session)

    session.query().filter().first.assert_called_once()

    assert isinstance(found_album, models.Album)
    assert found_album == db_album


def test_read_album(session, db_album, find_album_mock, jsonable_encoder_mock):
    albums.find_album = find_album_mock
    albums.jsonable_encoder = jsonable_encoder_mock

    read_album = albums.read_album(1, session)

    albums.find_album.assert_called_once_with(1, session)
    albums.jsonable_encoder.assert_called_once_with(db_album)

    assert isinstance(read_album, schemas.Album)
    assert read_album.id == 1
    assert read_album.title == "Test Album"
    assert read_album.release_date == datetime.date.today()
    assert read_album.artist_id == 1


def test_update_album(session, db_album, find_album_mock, jsonable_encoder_mock_updated, album_update_schema):
    albums.find_album = find_album_mock
    session.commit.return_value = None
    session.refresh.return_value = None
    albums.jsonable_encoder = jsonable_encoder_mock_updated

    updated_album = albums.update_album(1,
                                        album_update_schema,
                                        session)

    albums.find_album.assert_called_once_with(1, session)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(db_album)
    albums.jsonable_encoder.assert_called_once_with(db_album)

    assert isinstance(updated_album, schemas.Album)
    assert updated_album.id == 1
    assert updated_album.title == "Updated Test Album"
    assert updated_album.release_date == datetime.date(2000, 1, 1)
    assert updated_album.artist_id == 1


def test_delete_album(session, db_album, find_album_mock, jsonable_encoder_mock):
    albums.find_album = find_album_mock
    session.delete.return_value = None
    session.commit.return_value = None
    albums.jsonable_encoder = jsonable_encoder_mock

    deleted_album = albums.delete_album(1, session)

    albums.find_album.assert_called_once_with(1, session)
    session.delete.assert_called_once_with(db_album)
    session.commit.assert_called_once()
    albums.jsonable_encoder.assert_called_once_with(db_album)

    assert isinstance(deleted_album, schemas.Album)
    assert deleted_album.id == 1
    assert deleted_album.title == "Test Album"
    assert deleted_album.release_date == datetime.date.today()
    assert deleted_album.artist_id == 1
