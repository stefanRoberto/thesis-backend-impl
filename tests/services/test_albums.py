import datetime

import pytest
from unittest.mock import MagicMock, ANY

from app import models, schemas
from app.services import albums


@pytest.fixture
def jsonable_encoder_mock():
    return MagicMock(return_value={"id": 1,
                                   "title": "Test Album",
                                   "release_date": datetime.date.today().isoformat(),
                                   "artist_id": 1})


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
